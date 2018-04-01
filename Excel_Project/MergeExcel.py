import xlrd
from xlutils.copy import copy



def ReadMapping(filename):
    MappingFile = xlrd.open_workbook(filename, "rb")
    Sheets = MappingFile.sheet_names()
    Data = []
    StartQuestion = -1
    for SheetName in Sheets:
        sh = MappingFile.sheet_by_name(SheetName)
        for RowNum in range(sh.nrows):
            RowValues = sh.row_values(RowNum)
            if 'Short Name' in RowValues:
                #print 'yes'
                #print rownum
                StartQuestion = RowNum
                #print sh.ncols
            if RowNum > StartQuestion and StartQuestion != -1:
                Data.append(RowValues)
    return Data

MapData =  ReadMapping("mapping.xlsx")

def ReadAnswerAndWriteToTarget(AnswerFile,TargetFile,QuestionData):
    AnswerSheet = xlrd.open_workbook(AnswerFile, "rb")
    AnswerSheetName = AnswerSheet.sheet_names()

    for Question in QuestionData:
        if Question[3]:
            # print question_detail[4].find('.')
            QuestionNo = Question[3]
            QaPointer = Question[0]
            AnswerSheetPrefix = Question[3][:Question[3].find('.') + 1]
            for EachAnswerSheet in AnswerSheetName:
                if EachAnswerSheet.startswith(AnswerSheetPrefix):
                    SpecifiedAnswerSheet = AnswerSheet.sheet_by_name(EachAnswerSheet)
                    for row in range(SpecifiedAnswerSheet.nrows):

                        if SpecifiedAnswerSheet.row_values(row)[0] == QuestionNo:
                            #print SpecifiedAnswerSheet.row_values(row)
                            QaSheet = xlrd.open_workbook(TargetFile, "rb")
                            #QASheetName = QA.sheet_names()
                            SheetQA = QaSheet.sheet_by_name("Sheet1")
                            for qa_row in range(SheetQA.nrows):
                                if SheetQA.row_values(qa_row)[0] == QaPointer:
                                    #SheetQA.row_values(qa_row).append('ow')
                                    #print sheetQA.row_values(qa_row)
                                    CopyOfQa = copy(QaSheet)

                                    FinalSheet = CopyOfQa.get_sheet(0)
                                    print SpecifiedAnswerSheet.row_values(row)[2]
                                    print qa_row
                                    FinalSheet.write(qa_row, 2, SpecifiedAnswerSheet.row_values(row)[2])
                                    CopyOfQa.save(TargetFile)
                            break


ReadAnswerAndWriteToTarget("final.xlsx","QA.xlsx",MapData)

