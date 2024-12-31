import csv


# 新しく追加するデータ（例）
new_rows = []


# k=47
# for i in range(1,k+3,2):
# #                    1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 
#   if i==1:
#     new_rows.append([k, i, 0, 0,"","","","","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
#   elif i==3:
#     new_rows.append([k, i, 0, 3,"","","","[Toda3]Th4.3(2), \ E^{2}\\alpha_{12}(3)=3\\alpha_{12}{'}(5)","","[Toda3]Th4.3(3), \ H(\\alpha_{12}(3))=A_{11}","","","","83","1 0 0 0 0 0 0 0 0 0 0 0"])
#   else:
#     if i==5:
#       new_rows.append([k, i, 0, 9,"","","","","","[Toda3]Th4.3(3), \ H(\\alpha_{12}{'}(5))=A_{10}","","","","84","1 0 0 0 0 0 0 0 0 0 0 0"])
#     else:
#       new_rows.append([k, i, 0, 9,"","","","","","HE^{2}=0","","","","84","1 0 0 0 0 0 0 0 0 0 0 0"])
#   if i>=5:
#     if i==5:
#       new_rows.append([k, i, 1, 3,"","","","","","[Toda3]Th5.4(3), \ H(\\beta_{1}\\epsilon'(5))=A^{ {4} }","","","","3 56","0 1 0 0 0 0 0 0 0 0 0 0"])
#     else:
#       new_rows.append([k, i, 1, 3,"","","","","","","","","","3 56","0 1 0 0 0 0 0 0 0 0 0 0"])

#   if i==5:
#     new_rows.append([k, i, 2, 3,"","","","E^{2}P=0","","[Toda3]Th5.4(2), \ H\\Delta\\xi(ab_{2},bb_{2})=ABB_{2}","","","","85","0 0 1 0 0 0 0 0 0 0 0 0"])
#   if i==7:
#     new_rows.append([k, i, 2, 3,"","","","","","[Toda3]Th5.4(2), \ H\\xi(ab_{2},bb_{2})=bb_{2}","","","","85","0 0 1 0 0 0 0 0 0 0 0 0"])
#   if i==9:
#     new_rows.append([k, i, 2, 3,"","","","E^{2}P=0","","HE^{2}=0","","","","85","0 0 1 0 0 0 0 0 0 0 0 0"])

k=48
for i in range(1,k+3,2):
#                    1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 
  if i<=3:
    new_rows.append([k, i, 0, 0,"","","","","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])
  elif i==5:
    new_rows.append([k, i, 0, 3,"","","","E^{2}P=0","","[Toda3]Th5.4(2), \ H \\Delta\\xi(b^{3},e')=B^{4}","","","","86","1 0 0 0 0 0 0 0 0 0 0 0"])
  elif i==7:
    new_rows.append([k, i, 0, 3,"","","","","","[Toda3]Th5.4(2), \ H \\xi(b^{3},e')=e'","","","","86","1 0 0 0 0 0 0 0 0 0 0 0"])
  elif i==9:
    new_rows.append([k, i, 0, 3,"","","","E^{2}P=0","","HE^{2}=0","","","","86","1 0 0 0 0 0 0 0 0 0 0 0"])

  elif i==15:
    new_rows.append([k, i, 0, 3,"","","","","","[Toda3]Th5.4(2), \ H \\xi(AB,B^{2})=B^{2}","","","","87","1 0 0 0 0 0 0 0 0 0 0 0"])
  elif i==17:
    new_rows.append([k, i, 0, 3,"","","","E^{2}P=0","","HE^{2}=0","","","","87","1 0 0 0 0 0 0 0 0 0 0 0"])
  elif i==19:
    new_rows.append([k, i, 0, 3,"","","","E^{2}P=0","","[Toda3]Th5.4(2), \ HP(b)=ab","","","","88","1 0 0 0 0 0 0 0 0 0 0 0"])
  
  else:
    new_rows.append([k, i, 0, 0,"","","","","","","","","","0","1 0 0 0 0 0 0 0 0 0 0 0"])




# new_rows = [
# #  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 
#   [k, i, 0, 3,"","","","","","","","","","","1 0 0 0 0 0 0 0 0 0 0 0"] for i in range(1,k+3,2)
# ]

# ファイル名
input_file = 'sphere3.csv'
output_file = 'sphere3.csv'

# CSVファイルを読み込み
with open(input_file, 'r', encoding='utf-8') as f:
  reader = list(csv.reader(f))

insert_position = 807
updated_data = reader[:insert_position] + new_rows + reader[insert_position:]

# 新しいCSVファイルとして保存
with open(output_file, 'w', encoding='utf-8', newline='') as f:
  writer = csv.writer(f)
  writer.writerows(updated_data)

print(f"{input_file}の754行目に10行を追加し、'{output_file}'に保存しました。")
