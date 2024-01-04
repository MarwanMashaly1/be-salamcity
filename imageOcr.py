# import easyocr

# def imageOcr(img):
#     reader = easyocr.Reader(['en', 'ar'])
#     result = reader.readtext(img)
#     return result

# def filterText(events):
#     for event in events:
#             img = event[1].split("img: ")[1]
#             desc_list = imageOcr(img)
#             clean_desc = []
#             for entry in desc_list:
#                 for i in range(0, len(entry)-1):
#                     if (type(entry[i]) == float and type(entry[i+1]) == str):
#                         if (entry[i] > 0.50):
#                             print(entry[i+1])
#                             clean_desc.append(entry[i+1])
#                 # if (entry[4].isdigit and entry[4] > 0.75 and entry[3].isalpha):
#                 #     clean_desc.append(entry[4])
#             img_desc = ''.join(map(str, imageOcr(img)))
            
#             event.append(["img_desc: " + img_desc])