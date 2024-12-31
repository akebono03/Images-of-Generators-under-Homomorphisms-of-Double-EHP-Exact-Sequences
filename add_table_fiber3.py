import csv


# 新しく追加するデータ（例）
new_rows = []


# k=47
# for i in range(1,k+3,2):
# #                    1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 
#   if i==5:
#     new_rows.append([k, i, 0, 3,"BB_{2}","[Toda3]Th5.4(2), \ P(BB_{2})=\\Delta\\xi(ab_{2},bb_{2})","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
#     new_rows.append([k, i, 0, 3,"e'","PH=0","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
#   elif i==9:
#     new_rows.append([k, i, 0, 3,"ab_{2}","[Toda3]Th5.4(2), \ P(ab_{2})=E^{2}\\xi(ab_{2},bb_{2})","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
#   elif i==13:
#     new_rows.append([k, i, 0, 3,"B^{2}","PH=0","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
#   elif i==17:
#     new_rows.append([k, i, 0, 3,"ab","PH=0","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
#   else:
#     new_rows.append([k, i, 0, 0,"0","","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])

k=48
for i in range(1,k+3,2):
#                    1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 
  if i==1:
    new_rows.append([k, i, 0, 3,"b^{2}b_{2}","PH=0","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
    new_rows.append([k, i, 0, 3,"AE_{2}","PH=0","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
  elif i==3:
    new_rows.append([k, i, 0, 3,"e_{2}","PH=0","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
  elif i==5:
    new_rows.append([k, i, 0, 3,"E'","[Toda3]Th5.4(2), \ P(E')=\\Delta\\xi(b^{3},e')","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
    new_rows.append([k, i, 0, 3,"e_{1}","PH=0","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
  elif i==9:
    new_rows.append([k, i, 0, 3,"AB_{2}","PH=0","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
    new_rows.append([k, i, 0, 3,"b^{3}","[Toda3]Th5.4(2), \ P(b^{3})=E^{2}\\xi(b^{3},e')","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
  elif i==11:
    new_rows.append([k, i, 0, 3,"b_{2}","PH=0","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
  elif i==17:
    new_rows.append([k, i, 0, 3,"AB","[Toda3]Th5.4(2), \ P(AB)=E^{2}\\xi(AB,B^{2})","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
  elif i==19:
    new_rows.append([k, i, 0, 3,"b","[Toda3]Th5.4(2), \ P(b)\\ne0","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
  else:
    new_rows.append([k, i, 0, 0,"0","","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])



# new_rows = [
# #  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 
#   [k, i, 0, 3,"","","","","","","","","","","1 0 0 0 0 0 0 0 0 0 0 0"] for i in range(1,k+3,2)
# ]

# ファイル名
input_file = 'fiber3.csv'
output_file = 'fiber3.csv'
# output_file = 'fiber3_.csv'

# CSVファイルを読み込み
with open(input_file, 'r', encoding='utf-8') as f:
  reader = list(csv.reader(f))

insert_position = 821
updated_data = reader[:insert_position] + new_rows + reader[insert_position:]

# 新しいCSVファイルとして保存
with open(output_file, 'w', encoding='utf-8', newline='') as f:
  writer = csv.writer(f)
  writer.writerows(updated_data)

print(f"{input_file}の754行目に10行を追加し、'{output_file}'に保存しました。")
