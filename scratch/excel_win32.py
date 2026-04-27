import win32com.client as win32

# 1. Initialize the Excel application
# Use DispatchEx to ensure a new instance is started if needed
excel = win32.gencache.EnsureDispatch('Excel.Application')

# 2. Make Excel visible (optional, set to False to run in background)
excel.Visible = True

# 3. Open a specific workbook
# Use raw strings (r'') for Windows file paths to handle backslashes correctly
file_path = r'C:\path\to\your\file.xlsx'
workbook = excel.Workbooks.Open(file_path)

# 4. Access a specific sheet
sheet = workbook.Worksheets('Sheet1')

# Example: Read a value from cell A1
print(sheet.Cells(1, 1).Value)

# 5. Clean up (optional)
# workbook.Close(SaveChanges=True)
# excel.Quit()