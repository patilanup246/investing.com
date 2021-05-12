import os
import requests
from bs4 import BeautifulSoup as soup


def text_scrap():
    try:
        url = str(input("Enter url scrap for: ")).strip()
        if url.lower().startswith("https://"):
            pass
        else:
            print("wrong input url. ")
            exit()

        #url = "https://www.sec.gov/Archives/edgar/data/200406/000020040620000010/form10-k20191229.htm"

        file_name = "_"+ str(url.split("/")[-1].replace(".", "-").strip()) +"_.txt"

        r = requests.get(url)

        page_soup = soup(r.text, "html.parser")

        html_body = page_soup.findAll("div", {"style": "font-family:Times New Roman;font-size:10pt;"})

        if len(html_body) > 0:
            table_tag = "padding-left:0px;text-indent:0px;line-height:normal;padding-top:10px;"

            pg_no_tag = "text-align:center;"
            txt_sk = "line-height:120%;text-align:center;font-size:10pt;"

            #txt_sk_2 = "line-height:120%;font-size:10pt;"

            i = 1
            bool_txt = False
            with open(file_name, "w", encoding='utf-8') as f:
                for body_txt in html_body:
                    try:
                        for main_txt in body_txt.contents:
                            try:
                                try:
                                    if main_txt["style"] == table_tag or main_txt_2["style"] == txt_sk:
                                        continue
                                except:
                                    pass

                                if len(main_txt) > 1:
                                    for main_txt_2 in main_txt.contents:
                                        try:
                                            if main_txt_2["style"] == table_tag or main_txt_2["style"] == txt_sk:
                                                if i == 1:
                                                    pass
                                                else:
                                                    continue
                                            elif main_txt_2["style"] == pg_no_tag:
                                                continue
                                            file_txt = main_txt_2.text.strip().replace("®", "").replace("•", "")

                                            if file_txt.upper().startswith("PART IV"):
                                                exit()
                                            elif file_txt.upper().startswith("PART I"):
                                                i += 1
                                                bool_txt = True
                                            if bool_txt == True:
                                                if len(file_txt) > 0:
                                                    f.write(file_txt + "\n")
                                                    print(file_txt)
                                        except:
                                            pass

                                else:
                                    if main_txt["style"] == table_tag or main_txt["style"] == txt_sk:
                                        if i == 1:
                                            pass
                                        else:
                                            continue
                                    elif main_txt["style"] == pg_no_tag:
                                        continue

                                    file_txt = main_txt.text.strip().replace("®", "").replace("•", "")

                                    if file_txt.upper().startswith("PART IV"):
                                        exit()
                                    elif file_txt.upper().startswith("PART I"):
                                        i += 1
                                        bool_txt = True
                                    if bool_txt == True:
                                        if len(file_txt) > 0:
                                            f.write(file_txt + "\n")
                                            print(file_txt)
                            except:
                                pass
                    except:
                        pass
        else:
            lst_final = []
            fst_result = page_soup.findAll("div", {"style": "clear:both;max-width:100%;position:relative;min-height:10.35pt;"})

            div_92_result = page_soup.findAll("div", {"style": "clear:both;max-width:100%;position:relative;"})

            try:
                lst_final.append(fst_result[1])
            except:
                pass

            for i in div_92_result:
                lst_final.append(i)

            table_txt = "border-collapse:collapse;font-size:16pt;margin-left:auto;margin-right:auto;padding-left:0pt;padding-right:0pt;width:79.99%;"
            table_txt_2 = "border-collapse:collapse;font-size:16pt;margin-left:auto;margin-right:auto;padding-left:0pt;padding-right:0pt;width:100%;"

            with open(file_name, "w", encoding='utf-8') as f:
                for file_text_lst in lst_final:
                    if file_text['style'] == table_txt.lower():
                        continue
                    if file_text['style'] == table_txt_2.lower():
                        continue

                    for file_text in file_text_lst:
                        try:
                            if file_text['style'] == table_txt.lower():
                                continue
                            if file_text['style'] == table_txt_2.lower():
                                continue
                            new_txt = file_text.text.strip()
                            if new_txt.upper().startswith("PART IV"):
                                print("hi")
                                exit()
                            else:
                                tt_txt = file_text.text.strip()
                                if len(tt_txt) > 0:
                                    f.write(tt_txt + "\n")
                        except:
                            pass

    except:
        pass


if __name__ == '__main__':
    text_scrap()

