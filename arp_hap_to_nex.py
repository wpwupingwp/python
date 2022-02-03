#!/usr/bin/python3

from pathlib import Path
from tkinter import messagebox, filedialog
from tkinter import ttk
import tkinter as tk

import argparse


def wlabel(window, text, row, column=0, width=25, padx=0, pady=0, sticky='ew',
           **kargs):
    """
    Generate and pack labels.
    """
    label = ttk.Label(window, text=text, width=width, anchor=tk.CENTER,
                      **kargs)
    label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    return label


def fentry(window, row, column, default='', padx=0, pady=0):
    """
    Generate and pack entrys.
    Fill with default string.
    """
    entry = ttk.Entry(window)
    entry.insert(0, default)
    entry.grid(row=row, column=column, padx=padx, pady=pady)
    return entry


def open_file(title, entry, write=False):
    def func():
        if write:
            a= filedialog.asksaveasfilename(title=title)
        else:
            a = filedialog.askopenfilename(title=title)
        entry.delete(0, 'end')
        entry.insert(0, a)
    return func


def ui():
    def submit():
        arg_str = ''
        arp = arp_entry.get()
        hap = hap_entry.get()
        out = out_entry.get()
        if not all([arp, hap, out]):
            messagebox.showinfo(message='Input is required!')
        combine(arp, hap, out)
        messagebox.showinfo(message='Done.')
        return

    global root
    root = tk.Tk()
    root.attributes('-topmost', 'true')
    root.title('arp_hap_to_nex')
    root.geometry('500x200')
    root_frame = ttk.Frame(root)
    root_frame.place(relx=0.5, rely=0.5, anchor='center')
    row = 0
    wlabel(root_frame, 'arp file', row=row, column=1)
    arp_entry = fentry(root_frame, row=row, column=2)
    arp_button = ttk.Button(root_frame, text='Open', command=open_file(
        'arp file', arp_entry))
    arp_button.grid(row=row, column=3)
    row += 1
    wlabel(root_frame, 'hap file', row=row, column=1)
    hap_entry = fentry(root_frame, row=row, column=2)
    hap_button = ttk.Button(root_frame, text='Open', command=open_file(
        'hap file', hap_entry))
    hap_button.grid(row=row, column=3)
    row += 1
    wlabel(root_frame, 'Output', row=row, column=1)
    out_entry = fentry(root_frame, row=row, column=2)
    o_button = ttk.Button(root_frame, text='Open',
                          command=open_file('output file', out_entry,
                                            write=True))
    o_button.grid(row=row, column=3)
    row += 1
    ok = ttk.Button(root_frame, text='Enter', command=submit)
    ok.grid(row=row, column=0, columnspan=3, sticky='EW', padx=50, pady=10)
    root.mainloop()


def write_hap(hap_file: Path, nex_file: Path) -> list:
    samples = []
    with open(hap_file, 'r') as hap, open(nex_file, 'w') as nex:
        ntax = 0
        for line in hap:
            ntax += 1
        nchar = len(line.strip().split(' ')[-1])
        hap.seek(0)
        data_head = f'''
#NEXUS
Begin Data;
Dimensions ntax={ntax} nchar={nchar};
Format datatype=DNA missing=N gap=-;
Matrix
'''
        nex.write(data_head)
        hap.seek(0)
        for line in hap:
            samples.append(line.split(' ')[0])
            nex.write(line)
        data_tail = '''
;
END;
'''
        nex.write(data_tail)
    return samples


def write_arp(arp_file: Path, nex_file: Path, samples: list) -> Path:
    labels = 'max tra mul cath dai ade'.split()
    with open(arp_file, 'r') as arp, open(nex_file, 'a') as nex:
        head = '''
        
Begin Traits;
Dimensions NTraits=6;
format labels=yes missing=? separator=Tab;
TraitLabels	max	tra	mul	cath	dai	ade;
Matrix
'''
        nex.write(head)
        for line in arp:
            if line.startswith('[[Samples]]'):
                break
        traits_dict = {i: None for i in labels}
        for line in arp:
            if len(line.strip()) == 0:
                break
            if line.strip().startswith('SampleName'):
                name = line.split('"')[1]
            elif line.strip().startswith('SampleSize'):
                continue
            elif line.strip().startswith('SampleData'):
                record = []
            elif line.strip().startswith('}'):
                traits_dict[name] = record
            else:
                record.append(line.strip().split(' '))
        sample_traits = dict()
        for sample in samples:
            record = dict()
            for label, record in traits_dict:
                for r in record:
                    if r[0] == sample:
                        record[label] = r[1]
            content = '\t'.join([record[i] for i in label])
            nex.write(f'{sample}\t{content}\n')
        tail = '''
;
END; 
'''
        nex.write(tail)
        return nex_file


def combine(arp, hap, out):
    arp = Path(arp)
    hap = Path(hap)
    out = Path(out)
    samples = write_hap(hap, out)
    write_arp(arp, out, samples)
    return



def parse_args():
    arg = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=main.__doc__)
    arg.add_argument('-arp', help='arp file')
    arg.add_argument('-hap', help='hap file')
    arg.add_argument('-out', help='out file')
    return arg.parse_args()


def main():
    """
    Combine ".arp" and ".hap" files generated from DNASP to NEXUS file for
    popart.
    """
    arg = parse_args()
    if arg.arp is None or arg.hap is None:
        ui()
    else:
        combine(arg.arp, arg.hap, arg.out)
        print('Done.')


if __name__ == '__main__':
    main()
