import xlrd
from xlutils.copy import copy


workbook = xlrd.open_workbook("mapping.xlsx","rb")
sheets = workbook.sheet_names()
required_data = []
start_question = -1
for sheet_name in sheets:
    sh = workbook.sheet_by_name(sheet_name)
    for rownum in range(sh.nrows):
        row_values = sh.row_values(rownum)
        #print row_valaues
        #print type(row_valaues)
        if 'Short Name' in row_values:
            print 'yes'
            print rownum
            start_question = rownum
            print sh.ncols
        #print row_valaues[1]
            #break
        if rownum> start_question and  start_question != -1:
            required_data.append(row_values)
#required_data= [x for x in required_data if x]
print required_data
AnswerSheet = xlrd.open_workbook("final.xlsx","rb")
AnswerSheetName = AnswerSheet.sheet_names()

for question_detail in required_data:
    if question_detail[3]:
        #print question_detail[4].find('.')
        question_no = question_detail[3]
        qa_no = question_detail[0]
        answer_no =  question_detail[3][:question_detail[3].find('.')+1]
        for answer_sheet in AnswerSheetName:
            if answer_sheet.startswith(answer_no):
                sheet = AnswerSheet.sheet_by_name(answer_sheet)
                for row in range(sheet.nrows):

                    if sheet.row_values(row)[0]  == question_no:
                        print sheet.row_values(row)
                        QA = xlrd.open_workbook("QA.xlsx", "rb")
                        QASheetName = QA.sheet_names()
                        sheetQA = QA.sheet_by_name("Sheet1")
                        for qa_row in range(sheetQA.nrows):
                            if sheetQA.row_values(qa_row)[0] == qa_no:
                                sheetQA.row_values(qa_row).append('ow')
                                print sheetQA.row_values(qa_row)
                                wb = copy(QA)

                                s = wb.get_sheet(0)
                                print sheet.row_values(row)[2]
                                print qa_row
                                s.write(qa_row, 2, sheet.row_values(row)[2])
                                wb.save('QA.xlsx')
                        break
                #break

        #break