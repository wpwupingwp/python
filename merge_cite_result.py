import argparse
import sys
import warnings
from pathlib import Path

# ensure pands dependencies exist
import xlrd
import lxml
import pandas as pd

warnings.filterwarnings('ignore')

def read_cnki_html(cnki_file):
    """
    Read CNKI HTML table file
    """
    print(f"Reading CNKI HTML file: {cnki_file}")
    
    try:
        # Try different encodings for HTML
        encodings_to_try = ['utf-8', 'gbk', 'gb2312', 'latin1']
        
        for encoding in encodings_to_try:
            try:
                html_tables = pd.read_html(cnki_file, encoding=encoding, header=0)
                print(f"Successfully read with {encoding} encoding")
                break
            except:
                continue
        else:
            # If all encodings fail, try without specifying encoding
            html_tables = pd.read_html(cnki_file)
        
        if not html_tables:
            raise ValueError("No table found in HTML file")
        
        # Usually the first table contains main data
        df_cnki = pd.DataFrame(html_tables[0])
        
        # Check if there are multiple tables
        if len(html_tables) > 1:
            print(f"Found {len(html_tables)} tables, using the first one")
        print(f"CNKI HTML table shape: {df_cnki.shape}")

        # Clean CNKI table special formats
        df_cnki = clean_cnki_dataframe(df_cnki)
        
        return df_cnki
        
    except Exception as e:
        print(f"Failed to read HTML file: {e}")
        print("Trying to read as text file and extract tables...")
        
        # Try reading as plain text file
        try:
            with open(cnki_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"File size: {len(content)} characters")
        except:
            try:
                with open(cnki_file, 'r', encoding='gbk') as f:
                    content = f.read()
                print(f"File size: {len(content)} characters (read with GBK)")
            except Exception as e2:
                print(f"Cannot read file: {e2}")
                raise ValueError(f"Cannot read CNKI file: {cnki_file}")
        
        # Try to extract tables from content
        try:
            tables = pd.read_html(content)
            if tables:
                print(f"Extracted {len(tables)} tables from content")
                df_cnki = tables[0]
                df_cnki = clean_cnki_dataframe(df_cnki)
                return df_cnki
        except Exception as e3:
            print(f"Cannot extract tables from content: {e3}")
        
        raise ValueError(f"Cannot process CNKI file: {cnki_file}")


def clean_cnki_dataframe(df):
    """
    Clean CNKI dataframe special formats
    """
    print("Cleaning CNKI data format...")
    
    # Create a copy to avoid modifying original
    # print(df.iloc[:2,:])
    df = df.copy()
    
    # 1. Check for multi-level column index (MultiIndex)
    if isinstance(df.columns, pd.MultiIndex):
        print("Detected multi-level column index, flattening...")
        # Merge multi-level columns into single level
        new_columns = []
        for col in df.columns:
            if isinstance(col, tuple):
                # Join tuple elements with '-', filter out None/empty
                col_str = '-'.join(filter(None, map(str, col))).strip()
                new_columns.append(col_str)
            else:
                new_columns.append(str(col))
        df.columns = new_columns
    
    # 2. Clean column names safely
    # print(f"Original columns: {list(df.columns)}")
    # Convert all column names to strings first
    df.columns = [str(col) for col in df.columns]
    # Then apply string operations safely
    df.columns = [col.strip() if isinstance(col, str) else str(col) for col in df.columns]
    # 3. Find and rename CNKI-specific Chinese/English column names
    cnki_column_mapping = {
        # Title related
        'Title': 'Title-题名',
        'Title-题名': 'Title-题名',
        '文章标题': 'Title-题名',
        '论文标题': 'Title-题名',
        
        # Author related
        '作者': 'Author-作者',
        'Author': 'Author-作者',
        'Author-作者': 'Author-作者',
        '著者': 'Author-作者',
        
        # Organization related
        '单位': 'Organ-单位',
        '机构': 'Organ-单位',
        'Organ': 'Organ-单位',
        'Organ-单位': 'Organ-单位',
        '作者单位': 'Organ-单位',
        
        # Source related
        '文献来源': 'Source-文献来源',
        '期刊': 'Source-文献来源',
        'Source': 'Source-文献来源',
        'Source-文献来源': 'Source-文献来源',
        '期刊名称': 'Source-文献来源',
        '来源': 'Source-文献来源',
        
        # Keywords related
        '关键词': 'Keyword-关键词',
        'Keywords': 'Keyword-关键词',
        'Keyword-关键词': 'Keyword-关键词',
        '关键字': 'Keyword-关键词',
        
        # Abstract related
        '摘要': 'Summary-摘要',
        'Abstract': 'Summary-摘要',
        'Summary': 'Summary-摘要',
        'Summary-摘要': 'Summary-摘要',
        '文章摘要': 'Summary-摘要',
        
        # Publication time related
        '发表时间': 'PubTime-发表时间',
        '出版时间': 'PubTime-发表时间',
        'PubTime': 'PubTime-发表时间',
        'PubTime-发表时间': 'PubTime-发表时间',
        '发表日期': 'PubTime-发表时间',
        '出版日期': 'PubTime-发表时间',
        
        # Year related
        '年': 'Year-年',
        'Year': 'Year-年',
        'Year-年': 'Year-年',
        '出版年': 'Year-年',
        
        # DOI related
        'DOI': 'DOI-DOI',
        'DOI-DOI': 'DOI-DOI',
        '数字对象标识符': 'DOI-DOI',
        
        # ISSN related
        'ISSN': 'ISSN-国际标准刊号',
        'ISSN-国际标准刊号': 'ISSN-国际标准刊号',
        '国际标准刊号': 'ISSN-国际标准刊号',
        
        # URL related
        '网址': 'URL-网址',
        'URL': 'URL-网址',
        'URL-网址': 'URL-网址',
        '链接': 'URL-网址',
        
        # Fund related
        '基金': 'Fund-基金',
        'Fund': 'Fund-基金',
        'Fund-基金': 'Fund-基金',
        '基金项目': 'Fund-基金',
        
        # Volume/Issue/Pages related
        '卷': 'Volume-卷',
        '期': 'Period-期',
        '页码': 'PageCount-页码',
        'Volume': 'Volume-卷',
        'Period': 'Period-期',
        'PageCount': 'PageCount-页码',
        'Volume-卷': 'Volume-卷',
        'Period-期': 'Period-期',
        'PageCount-页码': 'PageCount-页码',
    }
    
    # Apply column name mapping
    rename_dict = {}
    for old_col in df.columns:
        col_str = str(old_col).strip()
        
        # Try exact match first
        if col_str in cnki_column_mapping:
            rename_dict[old_col] = cnki_column_mapping[col_str]
            continue
    # Apply renaming
    if rename_dict:
        df = df.rename(columns=rename_dict)
    
    # 4. Clean data content safely
    print("Cleaning data content...")
    for col in df.columns:
        try:
            # Convert to string safely
            df[col] = df[col].astype(str)
            
            # Apply string operations only if it's actually a string column
            if df[col].dtype == 'object':
                # Replace NaN strings
                df[col] = df[col].replace(['nan', 'NaN', 'NaT', 'None', 'null', ''], pd.NA)
                
                # Remove spaces from string ends
                df[col] = df[col].str.strip()
        except Exception as e:
            print(f"Warning: Could not clean column '{col}': {e}")
            # Keep column as is if cleaning fails
    
    print(f"DataFrame shape after cleaning: {df.shape}")
    return df


def read_cnki(cnki_file: Path):
    # CNKI file (HTML or Excel)
    cnki_ext = Path(cnki_file).suffix.lower()

    if cnki_ext in ['.html', '.htm']:
        df_cnki = read_cnki_html(cnki_file)
    elif cnki_ext in ['.xls', '.xlsx']:
        print(f'CNKI custom export file uses .xls but is a html table!')
        df_cnki = read_cnki_html(cnki_file)
    else:
        # If it's an Excel file, read normally
        try:
            df_cnki = pd.read_excel(cnki_file)
            print(f"✓ CNKI records: {len(df_cnki)} (Excel format)")
        except:
            try:
                df_cnki = pd.read_excel(cnki_file)
                print(
                    f"✓ CNKI records: {len(df_cnki)} (Excel format with xlrd)")
            except Exception as e:
                print(f"✗ Cannot read CNKI file: {e}")
                # Create empty dataframe
                df_cnki = pd.DataFrame()
                print("⚠ Created empty DataFrame for CNKI")
    return df_cnki


def merge_cnki(cnki_files: list[Path]):
    df_list = []
    for cnki_file in cnki_files:
        df_cnki = read_cnki(cnki_file)
        print(f'Read {len(df_cnki)} CNKI records')
        df_list.append(df_cnki)
    df_cnki_merge = pd.concat(df_list)
    print(f'Merged CNKI records: {len(df_cnki_merge)}')
    return df_cnki_merge


def merge_tables(crossref_file: Path, endnote_file: Path, cnki_files: list[Path],
                 output_file):
    """
    Merge three tables, remove duplicates, and output as xlsx file
    Key fields include: DOI, Title, Authors, Year, Source, Abstract, Keywords
    """
    print("=" * 60)
    print("STARTING DATA MERGE PROCESS")
    print("=" * 60)
    
    # 1. Read data
    print("\n1. READING DATA...")
    
    # Crossref CSV file
    try:
        df_crossref = pd.read_csv(crossref_file, encoding='utf-8')
        print(f"✓ Crossref records: {len(df_crossref)}")
    except UnicodeDecodeError:
        # Try other encodings
        try:
            df_crossref = pd.read_csv(crossref_file, encoding='gbk')
            print(f"✓ Crossref records: {len(df_crossref)} (using GBK encoding)")
        except:
            df_crossref = pd.read_csv(crossref_file, encoding='latin1')
            print(f"✓ Crossref records: {len(df_crossref)} (using latin1 encoding)")
    
    # EndNote Excel file
    df_endnote = pd.read_excel(endnote_file)
    print(f"✓ EndNote records: {len(df_endnote)}")

    df_cnki = merge_cnki(cnki_files)
    print(f"✓ CNKI records: {len(df_cnki)}")
    
    # 2. Unify DOI column names
    print("\n2. UNIFYING DOI COLUMN NAMES...")
    
    # Crossref: DOI column already exists
    if 'DOI' not in df_crossref.columns:
        # Try to find DOI-related columns
        doi_cols = [col for col in df_crossref.columns if 'doi' in col.lower()]
        if doi_cols:
            df_crossref['DOI'] = df_crossref[doi_cols[0]]
            print(f"✓ Crossref: Found DOI in column '{doi_cols[0]}'")
        else:
            df_crossref['DOI'] = None
            print("⚠ Crossref: No DOI column found")
    else:
        print("✓ Crossref: DOI column exists")
    
    # EndNote: Find DOI column
    if 'DOI' not in df_endnote.columns:
        doi_cols_endnote = [col for col in df_endnote.columns if 'doi' in col.lower()]
        if doi_cols_endnote:
            df_endnote['DOI'] = df_endnote[doi_cols_endnote[0]]
            print(f"✓ EndNote: Found DOI in column '{doi_cols_endnote[0]}'")
        else:
            df_endnote['DOI'] = None
            print("⚠ EndNote: No DOI column found")
    else:
        print("✓ EndNote: DOI column exists")
    
    # CNKI: Find DOI column
    if not df_cnki.empty:
        if 'DOI-DOI' in df_cnki.columns:
            df_cnki['DOI'] = df_cnki['DOI-DOI']
            print("✓ CNKI: Found DOI in 'DOI-DOI' column")
        elif 'DOI' in df_cnki.columns:
            df_cnki['DOI'] = df_cnki['DOI']
            print("✓ CNKI: Found DOI in 'DOI' column")
        else:
            # Try to find columns containing DOI
            doi_cols_cnki = [col for col in df_cnki.columns if 'doi' in col.lower()]
            if doi_cols_cnki:
                df_cnki['DOI'] = df_cnki[doi_cols_cnki[0]]
                print(f"✓ CNKI: Found DOI in column '{doi_cols_cnki[0]}'")
            else:
                df_cnki['DOI'] = None
                print("⚠ CNKI: No DOI column found")
    else:
        df_cnki['DOI'] = None
        print("⚠ CNKI: Empty DataFrame, adding DOI column")
    
    # 3. Unify other key field column names
    print("\n3. UNIFYING KEY FIELD NAMES...")
    
    # Define mappings for each source
    field_mappings = {
        'crossref': {
            'title': ('Title', 'Title'),
            'authors': ('Authors', 'Authors'),
            'year': ('Year', 'Year'),
            'source': ('Source', 'Source'),
            'abstract': ('Abstract', 'Abstract'),
            'keywords': ('Keywords', 'Keywords'),
            'url': ('ArticleURL', 'ArticleURL'),
            'org': ('Affiliations', 'Affiliations'),
            'fund': ('Fund', 'Fund')

        },
        'endnote': {
            'title': ('Article Title', 'Title'),
            'authors': ('Authors', 'Authors'),
            'year': ('Publication Year', 'Year'),
            'source': ('Source Title', 'Source'),
            'abstract': ('Abstract', 'Abstract'),
            'keywords': ('Author Keywords', 'Keywords'),
            'url': ('ArticleURL', 'ArticleURL'),
            'org': ('Affiliations', 'Affiliations'),
            'fund': ('Funding Orgs', 'Fund')
        },
        'cnki': {
            'title': ('Title-题名', 'Title'),
            'authors': ('Author-作者', 'Authors'),
            'year': ('Year-年', 'Year'),
            'source': ('Source-文献来源', 'Source'),
            'abstract': ('Summary-摘要', 'Abstract'),
            'keywords': ('Keyword-关键词', 'Keywords'),
            'url': ('URL-网址', 'ArticleURL'),
            'org': ('Organ-单位', 'Affiliations'),
            'fund': ('Fund-基金', 'Fund')
        }
    }
    
    # Function to rename columns for a specific source
    def rename_columns(df, source_name):
        if df.empty:
            return df
            
        rename_dict = {}
        mappings = field_mappings.get(source_name, {})
        
        # Build rename dictionary
        for field_type, (old_col, new_col) in mappings.items():
            if old_col in df.columns:
                rename_dict[old_col] = new_col
                print(f"  ✓ {source_name}: '{old_col}' -> '{new_col}'")
            else:
                # Try to find similar columns
                possible_cols = [col for col in df.columns if field_type in col.lower()]
                if possible_cols:
                    rename_dict[possible_cols[0]] = new_col
                    print(f"  ✓ {source_name}: '{possible_cols[0]}' -> '{new_col}' (approximate match)")
        
        # Apply renaming
        if rename_dict:
            df = df.rename(columns=rename_dict)
        
        # Add data source identifier
        df['Data_Source'] = source_name
        
        return df
    
    print("Renaming Crossref columns:")
    df_crossref = rename_columns(df_crossref, 'crossref')
    
    print("\nRenaming EndNote columns:")
    df_endnote = rename_columns(df_endnote, 'endnote')
    
    print("\nRenaming CNKI columns:")
    df_cnki = rename_columns(df_cnki, 'cnki')
    

    # 4. Ensure all key field columns exist
    print("\n4. ENSURING ALL KEY FIELD COLUMNS EXIST...")
    
    # Define all key fields
    key_fields = ['DOI', 'Title', 'Authors', 'Year', 'Source', 'Abstract', 'Keywords', 'Data_Source','ArticleURL', 'Affiliations', 'Fund']
    
    for df, name in [(df_crossref, 'Crossref'), (df_endnote, 'EndNote'), (df_cnki, 'CNKI')]:
        if df.empty:
            print(f"  ⚠ {name}: Empty DataFrame, creating all columns")
            for field in key_fields:
                df[field] = None
            continue
            
        for field in key_fields:
            if field not in df.columns:
                print(f"  ⚠ {name}: Missing field '{field}', adding empty column")
                df[field] = None
            else:
                print(f"  ✓ {name}: Field '{field}' exists")
    
    # 5. Select columns to keep
    print("\n5. SELECTING COLUMNS TO MERGE...")
    
    # Define source-specific important columns
    source_specific_cols = {
        'crossref': ['FullTextURL', 'Publisher', 'ISSN', 'Cites', 
                    'Type', 'Volume', 'Issue', 'StartPage', 'EndPage'],
        'endnote': ['Times Cited, WoS Core', 'Publication Date', 'eISSN', 'Addresses', 
                    'Cited Reference Count', 'Publisher', 'Volume', 
                   'Issue', 'Start Page', 'End Page'],
        'cnki': ['CLC-中图分类号', 
                'ISSN-国际标准刊号', 'Volume-卷', 'Period-期', 'PageCount-页码',
                'PubTime-发表时间', 'FirstDuty-第一责任人']
        # 'cnki': ['Organ-单位', 'Fund-基金', 'URL-网址', 'CLC-中图分类号', 
        #         'ISSN-国际标准刊号', 'Volume-卷', 'Period-期', 'PageCount-页码',
        #         'PubTime-发表时间', 'FirstDuty-第一责任人']
    }
    
    # Select columns to keep for each source
    def select_columns(df, source_name):
        if df.empty:
            return df
            
        # Start with key fields
        cols_to_select = key_fields.copy()
        
        # Add source-specific columns that exist in the dataframe
        if source_name in source_specific_cols:
            for col in source_specific_cols[source_name]:
                if col in df.columns:
                    cols_to_select.append(col)
        
        # Ensure all selected columns exist in dataframe
        available_cols = []
        for col in cols_to_select:
            if col in df.columns:
                available_cols.append(col)
            else:
                # Add empty column if it doesn't exist
                df[col] = None
                available_cols.append(col)
        
        return df[available_cols]
    
    # Select columns for each dataframe
    print("Selecting columns for Crossref...")
    df_crossref_selected = select_columns(df_crossref, 'crossref')
    print(f"Crossref selected columns: {len(df_crossref_selected.columns)}")
    
    print("Selecting columns for EndNote...")
    df_endnote_selected = select_columns(df_endnote, 'endnote')
    print(f"EndNote selected columns: {len(df_endnote_selected.columns)}")
    
    print("Selecting columns for CNKI...")
    df_cnki_selected = select_columns(df_cnki, 'cnki')
    print(f"CNKI selected columns: {len(df_cnki_selected.columns)}")
    
    # 6. Merge all data
    print("\n6. MERGING ALL DATA...")
    
    # Check if any dataframes are empty
    if df_crossref_selected.empty and df_endnote_selected.empty and df_cnki_selected.empty:
        print("⚠ All dataframes are empty! Creating empty result.")
        merged_df = pd.DataFrame(columns=key_fields)
    else:
        # Merge all dataframes
        merged_df = pd.concat([df_crossref_selected, df_endnote_selected, df_cnki_selected], 
                             ignore_index=True, sort=False)
    
    print(f"✓ Total records after merging: {len(merged_df)}")
    print(f"✓ Total columns after merging: {len(merged_df.columns)}")
    
    # 7. Remove duplicates based on DOI
    print("\n7. REMOVING DUPLICATES BASED ON DOI...")
    
    def clean_doi(doi):
        """
        Clean DOI string
        """
        if pd.isna(doi):
            return None
        doi_str = str(doi).strip()
        if doi_str.lower() in ['nan', 'none', 'null', '', 'nan', 'nan']:
            return None
        # Remove URL prefixes if present
        doi_str = doi_str.replace('https://doi.org/', '').replace('http://doi.org/', '')
        doi_str = doi_str.replace('doi:', '').replace('DOI:', '')
        return doi_str.lower()
    
    # Clean DOI column
    merged_df['DOI_Clean'] = merged_df['DOI'].apply(clean_doi)
    
    # Count records with and without DOI
    doi_valid_count = merged_df['DOI_Clean'].notna().sum()
    doi_invalid_count = len(merged_df) - doi_valid_count
    
    print(f"✓ Records with valid DOI: {doi_valid_count} ({doi_valid_count/len(merged_df)*100:.1f}%)")
    print(f"✓ Records without DOI: {doi_invalid_count} ({doi_invalid_count/len(merged_df)*100:.1f}%)")
    
    # Separate records with and without DOI
    valid_doi_mask = merged_df['DOI_Clean'].notna()
    merged_df_valid = merged_df[valid_doi_mask].copy()
    merged_df_invalid = merged_df[~valid_doi_mask].copy()
    
    # Remove duplicates based on cleaned DOI (keep first occurrence)
    if not merged_df_valid.empty:
        original_count = len(merged_df_valid)
        merged_df_valid = merged_df_valid.drop_duplicates(subset='DOI_Clean', keep='first')
        duplicates_removed = original_count - len(merged_df_valid)
        print(f"✓ Removed {duplicates_removed} duplicate records with DOI")
    
    # Re-merge valid and invalid records
    final_df = pd.concat([merged_df_valid, merged_df_invalid], ignore_index=True)
    
    # Remove temporary DOI_Clean column
    final_df = final_df.drop('DOI_Clean', axis=1)
    
    print(f"✓ Records after deduplication: {len(final_df)}")
    print(f"✓ Total duplicates removed: {len(merged_df) - len(final_df)}")
    
    # 8. Optimize data format
    print("\n8. OPTIMIZING DATA FORMAT...")
    
    # Convert numeric columns
    numeric_columns = ['Year', 'Cites', 'Times Cited, WoS Core', 'Cited Reference Count']
    for col in numeric_columns:
        if col in final_df.columns:
            final_df[col] = pd.to_numeric(final_df[col], errors='coerce')
            print(f"✓ Converted '{col}' to numeric")
    
    # Clean text columns
    text_columns = ['Title', 'Authors', 'Source', 'Abstract', 'Keywords']
    for col in text_columns:
        if col in final_df.columns:
            # Convert to string and clean
            final_df[col] = final_df[col].astype(str)
            final_df[col] = final_df[col].str.strip()
            final_df[col] = final_df[col].replace(['nan', 'NaN', 'NaT', 'None', 'null'], pd.NA)
            print(f"✓ Cleaned '{col}' column")
    
    # 9. Sort and organize data
    print("\n9. ORGANIZING FINAL DATA...")
    
    # Sort by Year (descending) and Title (ascending)
    if 'Year' in final_df.columns:
        final_df = final_df.sort_values(['Year', 'Title'], ascending=[False, True])
        print("✓ Sorted by Year (descending) and Title (ascending)")
    
    # 10. fill url
    mask = final_df['ArticleURL'].isnull() & final_df['DOI'].notna()
    final_df.loc[mask, 'ArticleURL'] = 'https://doi.org/' + final_df.loc[mask, 'DOI'].astype(str)
    # Reset index
    final_df = final_df.reset_index(drop=True)
    
    # Add record ID
    final_df.insert(0, 'Record_ID', range(1, len(final_df) + 1))
    
    # 10. Save to Excel file
    print(f"\n10. SAVING TO EXCEL FILE: {output_file}")
    
    try:
        # Create Excel writer
        with pd.ExcelWriter(output_file) as writer:
            # Save main data
            final_df.to_excel(writer, index=False, sheet_name='Merged_Data')
            
            # Create summary sheet
            create_summary_sheet(writer, final_df, df_crossref, df_endnote, df_cnki)
            
            # Create statistics sheet
            create_statistics_sheet(writer, final_df)
            
            # Auto-adjust column widths
            workbook = writer.book
            for sheet_name in workbook.sheetnames:
                worksheet = workbook[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"✓ Successfully saved to {output_file}")
        
    except Exception as e:
        print(f"✗ Error saving to Excel: {e}")
        # Try to save as CSV as backup
        backup_file = output_file.replace('.xlsx', '.csv')
        final_df.to_csv(backup_file, index=False, encoding='utf-8-sig')
        print(f"✓ Saved backup CSV file: {backup_file}")
    
    # 11. Print final statistics
    print("\n" + "=" * 60)
    print("FINAL STATISTICS")
    print("=" * 60)
    
    print(f"\n📊 RECORD COUNTS:")
    print(f"   Crossref: {len(df_crossref):6d} records")
    print(f"   EndNote:  {len(df_endnote):6d} records")
    print(f"   CNKI:     {len(df_cnki):6d} records")
    print(f"   Merged:   {len(final_df):6d} records")
    
    print(f"\n🎯 DUPLICATES REMOVED:")
    print(f"   Total removed: {len(merged_df) - len(final_df):6d} records")
    
    print(f"\n🔍 DATA SOURCE DISTRIBUTION:")
    if 'Data_Source' in final_df.columns:
        source_counts = final_df['Data_Source'].value_counts()
        for source, count in source_counts.items():
            percentage = count / len(final_df) * 100
            print(f"   {source.upper():10s}: {count:6d} ({percentage:.1f}%)")
    
    print(f"\n📈 DOI STATISTICS:")
    if 'DOI' in final_df.columns:
        doi_count = final_df['DOI'].notna().sum()
        no_doi_count = len(final_df) - doi_count
        print(f"   With DOI:    {doi_count:6d} ({doi_count/len(final_df)*100:.1f}%)")
        print(f"   Without DOI: {no_doi_count:6d} ({no_doi_count/len(final_df)*100:.1f}%)")
    
    print(f"\n📋 FIELD COMPLETENESS:")
    fields_to_check = ['Title', 'Authors', 'Year', 'Source', 'Abstract', 'Keywords']
    for field in fields_to_check:
        if field in final_df.columns:
            count = final_df[field].notna().sum()
            percentage = count / len(final_df) * 100 if len(final_df) > 0 else 0
            print(f"   {field:10s}: {count:6d} ({percentage:.1f}%)")
    
    print(f"\n💾 OUTPUT FILE: {output_file}")
    print(f"   Total columns: {len(final_df.columns)}")
    print(f"   File size: {Path(output_file).stat().st_size / 1024:.1f} KB" if Path(output_file).exists() else "   File not created")
    
    return final_df

def create_summary_sheet(writer, final_df, df_crossref, df_endnote, df_cnki):
    """
    Create summary sheet in Excel file
    """
    # Prepare summary data
    summary_data = {
        'Metric': [
            'Total Records (Crossref)',
            'Total Records (EndNote)',
            'Total Records (CNKI)',
            'Total Records (Merged)',
            'Unique Records (After Deduplication)',
            'Duplicate Records Removed',
            'Records with DOI',
            'Records without DOI',
            'Records from Crossref',
            'Records from EndNote',
            'Records from CNKI'
        ],
        'Value': [
            len(df_crossref),
            len(df_endnote),
            len(df_cnki),
            len(df_crossref) + len(df_endnote) + len(df_cnki),
            len(final_df),
            (len(df_crossref) + len(df_endnote) + len(df_cnki)) - len(final_df),
            final_df['DOI'].notna().sum() if 'DOI' in final_df.columns else 0,
            len(final_df) - final_df['DOI'].notna().sum() if 'DOI' in final_df.columns else len(final_df),
            len(final_df[final_df['Data_Source'] == 'crossref']) if 'Data_Source' in final_df.columns else 0,
            len(final_df[final_df['Data_Source'] == 'endnote']) if 'Data_Source' in final_df.columns else 0,
            len(final_df[final_df['Data_Source'] == 'cnki']) if 'Data_Source' in final_df.columns else 0
        ]
    }
    
    df_summary = pd.DataFrame(summary_data)
    df_summary.to_excel(writer, index=False, sheet_name='Summary')


def create_statistics_sheet(writer, final_df):
    """
    Create statistics sheet in Excel file
    """
    statistics_data = []
    
    # Field completeness statistics
    if len(final_df) > 0:
        for column in final_df.columns:
            if column not in ['Record_ID', 'Data_Source']:
                non_null = final_df[column].notna().sum()
                percentage = non_null / len(final_df) * 100
                statistics_data.append({
                    'Field': column,
                    'Non-Null Count': non_null,
                    'Null Count': len(final_df) - non_null,
                    'Completeness %': percentage
                })
    
    df_stats = pd.DataFrame(statistics_data)
    df_stats.to_excel(writer, index=False, sheet_name='Statistics')


def parse_arg():
    """
    Parse command line arguments using argparse
    """
    parser = argparse.ArgumentParser(
        description='Merge academic literature data from Crossref/Google Scholar, EndNote, and CNKI sources',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -c crossref.csv -e endnote.xlsx -k cnki.html -o merged_output.xlsx
  %(prog)s --crossref crossref.csv --endnote endnote.xlsx --cnki cnki.xlsx --output results.xlsx

File formats:
  - Crossref: CSV file (comma-separated values)
  - EndNote: Excel file (.xlsx or .xls)
  - CNKI: HTML file (.html, .htm) or Excel file (.xlsx, .xls)
        """
    )

    # Positional arguments (for backward compatibility)
    parser.add_argument('-c', '--crossref', dest='crossref',
        help='Crossref data file in CSV format (alternative to positional argument)' )
    parser.add_argument('-e', '--endnote', dest='endnote',
        help='EndNote data file in Excel format (alternative to positional argument)' )
    parser.add_argument('-k', '--cnki', dest='cnki', nargs='*',
                         help='CNKI data file in HTML or Excel format (alternative to positional argument)' )
    parser.add_argument('-o', '--output', default='merged_literature_data.xlsx',
        help='Output Excel file name (default: merged_literature_data.xlsx)' )
    return parser.parse_args()


def init_arg(arg):
    arg.crossref = Path(arg.crossref).resolve()
    arg.endnote = Path(arg.endnote).resolve()
    arg.cnki = [Path(i).resolve() for i in arg.cnki]

    for i in (arg.crossref, arg.endnote, *arg.cnki):
        if not i.exists():
            print(f'Cannot find {i}')
            sys.exit(-1)
    return arg


def main():
    """
    Main function to run the merge script
    """
    arg = parse_arg()
    arg = init_arg(arg)

    print("=" * 60)
    print("ACADEMIC LITERATURE DATABASE MERGER")
    print("=" * 60)
    print("This script merges data from Crossref, EndNote, and CNKI sources")
    print("and removes duplicates based on DOI.\n")
    
    print("📁 INPUT FILES:")
    print(f"   Crossref: {arg.crossref}")
    print(f"   EndNote:  {arg.endnote}")
    print(f"   CNKI:     {arg.cnki}")
    print(f"   Output:   {arg.output}\n")
    
    # Run the merge process
    try:
        result_df = merge_tables(arg.crossref, arg.endnote, arg.cnki, arg.output)
        print("\n✅ MERGE PROCESS COMPLETED SUCCESSFULLY!")
        print(f"📄 Output file: {arg.output}")
        
        # Display first few rows
        print("\n📊 PREVIEW OF MERGED DATA:")
        print("-" * 80)
        if not result_df.empty:
            print(result_df[['Record_ID', 'Title', 'Authors', 'Year', 'Data_Source']].head(3).to_string())
        else:
            print("No data available")
        print("-" * 80)
        
    except Exception as e:
        print(f"\n❌ ERROR: Merge process failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
