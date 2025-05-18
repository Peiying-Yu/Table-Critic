from thought.TableFV.utils.helper import table2string
from .get_info import get_table_log, replace_leaves_with_end
import json
import re
import random

random.seed(42)

vertical_expansion_few_shot = """You are organizing hierarchical categories and their associated few-shot examples. Currently, you have two lists of few-shot examples under the same category. Your task is to decide whether these two lists can be meaningfully split into two distinct subcategories.

Analyze the examples in the two lists to determine if there is a clear and meaningful distinction between them.
    - If a distinction exists, create two subcategories and assign each list to one of them.
    - If no clear distinction exists, retain both lists under the original parent category.
Provide a clear explanation for your decision on whether to split or merge the lists, based on their content.

Here are some examples:
Example 1:
Parent Category: sub-table error

List 1: [
\t"Original Table:\n/*\ncol   : goal | date         | location          | opponent | lineup              | min | assist/pass | score | result | competition\nrow 1 : 1    | may 9, 2004  | usaalbuquerque nm | mexico   | on 70' (off lilly)  | 19  | tarpley     | 3\u20130   | 3\u20130    | friendly\nrow 2 : 2    | jun 26, 2005 | usavirginia beach | canada   | 90.start            | 12  | unassisted  | 1\u20130   | 2\u20130    | friendly\nrow 3 : 3    | jan 30, 2007 | chnguangzhou      | china pr | 90.start            | 46+ | unassisted  | 1\u20130   | 2\u20130    | four nations tournament\nrow 4 : 4    | may 12, 2007 | usafrisco tx      | canada   | off 72' (on wagner) | 28  | tarpley     | 3\u20131   | 6\u20132    | friendly\nrow 5 : 5    | sep 18, 2007 | chnshanghai       | nigeria  | 90.start            | 1   | wambach     | 1\u20130   | 1\u20130    | world cup \u2013 group b\nrow 6 : 6    | sep 30, 2007 | chnshanghai       | norway   | 90.start            | 58  | unassisted  | 3\u20130   | 4\u20131    | world cup final - third place playoff\nrow 7 : 7    | aug 18, 2008 | chnbeijing        | japan    | 90.start            | 44  | rodriguez   | 2\u20131   | 4\u20132    | olympics tournament\nrow 8 : 8    | sep 20, 2008 | usabridgeview il  | ireland  | 90.start            | 19  | tarpley     | 1\u20130   | 2\u20130    | friendly\n*/\n\nStatement:\nchalupny scored in 4 consecutive friendly competitions\n\nReasoning Steps:\nStep 1: Select relevant rows.\nThe question aims to find out the number of consecutive friendly competitions in which Chalupny scored. We need to look at the rows where the competition type is \"friendly\" and check the dates to determine if they are consecutive. The relevant rows are row 1, row 2, and row 4. So we use f_select_row(row 1, row 2, row 4).\n\nStep 2: Filter out useless columns.\nsimilar words of the question link to columns :\nscored in -> goal\nconsecutive -> date\nfriendly competitions -> competition\ncolumn value link to columns :\nfriendly -> competition\nSo we use f_select_column(goal, date, competition).\n  \nStep 3: Group the column of competition. So we use f_group_column(competition).\n\nStep 4: After using f_select_row(row 1, row 2, row 4), f_select_column(goal, date, competition) and f_group_column(competition), we obtain the sub table:\n/*\ncol : goal |       date  | competition\nrow 1 : 1 | may 9, 2004 | friendly\nrow 2 : 2 | jun 26, 2005 | friendly\nrow 3 : 4 | may 12, 2007 | friendly\n*/\n/*\nGroup the rows according to column: competition.\nGroup ID | competition | Count\nGroup 1 | friendly | 3\n*/\nChalupny did not score in any consecutive friendly competitions. The gaps in dates between her goals indicate non-consecutive friendly matches.\n\nPrediction Answer:\nNO\n\nCritique:\nRow 8 was omitted in Step 1, despite satisfying the criteria. The reasoning only considers rows 1, 2, and 4, which makes Step 1 incomplete and therefore incorrect. Step 1 is incorrect.\n\nConclusion: [Incorrect] Step 1",
\t"Original Table:\n/*\ncol   : seasons | team                                  | ch.wins | promotions | relegations\nrow 1 : 5       | pistoia basket 2000                   | 0       | 0          | 0\nrow 2 : 4       | juve caserta basket                   | 0       | 1          | 0\nrow 3 : 3       | gruppo triboldi basket soresina       | 0       | 1          | 0\nrow 4 : 3       | nuova sebastiani rieti                | 1       | 1          | 0\nrow 5 : 3       | progresso castelmaggiore              | 0       | 0          | 0\nrow 6 : 3       | orlandina basket                      | 1       | 1          | 1\nrow 7 : 3       | sutor basket montegranaro             | 0       | 1          | 1\nrow 8 : 3       | virtus ragusa                         | 0       | 0          | 1\nrow 9 : 3       | robur basket osimo                    | 0       | 0          | 1\nrow 10 : 3       | reyer venezia                         | 0       | 1          | 0\nrow 11 : 3       | new basket brindisi                   | 1       | 2          | 0\n*/\n\nStatement:\nnew basket brindisi had more promotions than nuova sebastiani rieti\n\nReasoning Steps:\nStep 1: Select relevant rows.\nThe question aims to compare the number of promotions between Nuova Sebastiani Rieti and New Basket Brindisi. We need to locate the rows for these two teams and compare their \"promotions\" column values to determine which team had more promotions. So we use f_select_row(row 4, row 6)\n\nStep 2: Filter out useless columns.\nsimilar words of the question link to columns:\nhad the most promotions -> promotions\nbetween the two teams -> team\ncolumn value of the question link to columns:\nnuova sebastiani rieti -> team\nnew basket brindisi -> team\nsemantic sentence of the question link to columns:\nwho had the most promotions -> promotions\nSo we use f_select_column(team, promotions).\n\nStep 3: After using f_select_row(row 4, row 6) and f_select_column(team, promotions), we obtain the sub-table:\n/*\ncol   : team                   | promotions\nrow 1 : nuova sebastiani rieti | 1\nrow 2 : orlandina basket       | 1\n*/\nThe table does not include a row for \"new basket brindisi\". However, both \"nuova sebastiani rieti\" and \"orlandina basket\" have 1 promotion each. Since there is no comparison available for \"new basket brindisi\", we cannot determine if it has more promotions than \"nuova sebastiani rieti\". Based on the provided data, both teams mentioned have the same number of promotions.\n\nPrediction Answer: \nNO\n\nCritique: \nStep 1 correctly identifies the relevant row for the team Nuova Sebastiani Rieti. However, there is an issue because the row for New Basket Brindisi (row 11) is not included in the selected rows. Step 1 is incorrect.\n\nConclusion: [Incorrect] Step 1"
]
List 2: [
\t"Original Table:\n/*\ncol   : res. | record | opponent         | method                        | event                                        | date               | round | time | location                                | notes\nrow 1 : win  | 12-3   | mike hayes       | ko (punch)                    | ksw 25: khalidov vs. sakurai                 | december 7, 2013   | 1     | 1:12 | wroc\u0142aw, poland\nrow 2 : win  | 11\u20133   | nick moghadden   | tko (punches)                 | bellator 99                                  | september 13, 2013 | 1     | 3:22 | temecula, california, united states     | bellator debut\nrow 3 : loss | 10\u20133   | guto inocente    | decision (unanimous)          | strikeforce: barnett vs. cormier             | may 19, 2012       | 3     | 5:00 | san jose, california, united states     | light heavyweight debut\nrow 4 : win  | 10\u20132   | brett albee      | tko (strikes)                 | strikeforce: diaz vs. daley                  | april 9, 2011      | 1     | 1:46 | san diego, california, united states\nrow 5 : loss | 9\u20132    | lavar johnson    | ko (punches)                  | strikeforce challengers: bowling vs. voelker | october 22, 2010   | 1     | 2:17 | fresno, california, united states\nrow 6 : win  | 9\u20131    | eddie sapp       | submission (rear-naked choke) | native fighting championship 6               | august 14, 2010    | 1     | 2:01 | campo, california, united states\nrow 7 : loss | 8\u20131    | cody goodale     | decision (unanimous)          | gladiator challenge: maximum force           | april 25, 2010     | 3     | 5:00 | san jacinto, california, united states\n*/\n\nStatement:\nvirgil zwicker had 6 losses.\n\nReasoning Steps:\nStep 1: Select relevant rows.\nThe question aims to find out the number of losses Virgil Zwicker had based on the provided fight records. We need to count the rows where the \"res.\" column shows \"loss\".\nSo we use f_select_row(row 3, row 5, row 7).\n\nStep 2: Filter out useless columns.\nsimilar words of the question link to columns:\nloses -> record\ncolumn value of the question link to columns:\n10\u20133 -> record\nsemantic sentence of the question link to columns:\nNone\nSo we use f_select_column(record).\n\nStep 3: After using f_select_row(row 3, row 5, row 7) and f_select_column(record), we obtain the sub table:\n/*\ncol   : record\nrow 1 : 10\u20133\nrow 2 : 9\u20132\nrow 3 : 8\u20131\n*/\nThe provided table shows records of wins and losses but does not specify who the records belong to. However, if we assume that the table represents Virgil Zwicker's records, then we can deduce the number of losses from each record. The losses in the records are 3, 2, and 1 respectively. If we consider each row as a separate season or period, then the total number of losses would be the sum of these losses: 3 + 2 + 1 = 6.\n\nPrediction Answer:\nYES\n\nCritique:\nStep 1 correctly identifies the relevant rows where the \"res.\" column indicates a loss. The rows selected are indeed the ones where the outcome is a loss. Step 1 is correct.\nStep 2 incorrectly filters out the columns. The question asks for the number of losses, but the filtering step selects only the 'record' column, which combines wins and losses in a single string (e.g., \"10\u20133\"). This does not directly provide the number of losses. Instead, the 'res.' column should be used to count the losses directly. Step 2 is incorrect.\n\nConclusion: [Incorrect] Step 2"
]

Explanation:
The two lists can be meaningfully split into two distinct subcategories based on the types of errors they address:
List 1 (row error):
The examples in List 1 primarily deal with row selection issues.
The reasoning steps focus on identifying and selecting relevant rows from a table to answer specific questions. The critiques highlight errors in the selection process, such as omitting relevant rows or selecting incorrect ones.
This type of error pertains to problems in interpreting or handling rows in the table, making "row error" a suitable category.
List 2 (column error):
The examples in List 2 mainly involve column selection and interpretation issues.
The reasoning steps emphasize filtering or interpreting columns to extract necessary information. The critiques identify errors in selecting the correct columns or misinterpreting column data (e.g., incorrectly filtering or aggregating results from combined columns).
This aligns with issues related to column-level operations, justifying the "column error" category.

Determination:
List 1: <row error>
List 2: <column error>


Example 2:
Parent Category: final query error

List 1: [
\t"Original Table:\n/*\ncol   : date             | home team         | score | away team       | notes\nrow 1 : 17 december 2007 | foolad            | 4-4   | esteghlal ahvaz | foolad progress 8-7 on penalties\nrow 2 : 21 december 2007 | rah ahan          | 2-2   | steel azin      | rah ahan progress 5-2 on penalties\nrow 3 : 21 december 2007 | zob ahan          | 1-1   | esteghlal       | esteghlal progress 3-1 on penalties\nrow 4 : 21 december 2007 | bargh shiraz      | 1-0   | paykan tehran\nrow 5 : 21 december 2007 | shahin bushehr    | 2-2   | saba battery    | shahin bushehr progress 6-5 on penalties\nrow 6 : 24 december 2007 | pas hamedan       | 3-0   | persepolis\nrow 7 : 26 february 2008 | moghavemat sepasi | 1-2   | sepahan\nrow 8 : 4 march 2008     | sanaye arak       | 0-1   | pegah gilan\n*/\n\n\nStatement:\nthe average score of all home team members for all dates is 2.125\n\nReasoning Steps:\nStep 1: Add necessary columns to the table.\nThe question asks about the average score of all home team members for all dates. We need to know the score of each match, which is given in the \"score\" column. The scores are in the format home-team-score-away-team-score. We extract the home team score for each row and create a different column \"home team score\" for each row. The datatype is numerical. So we use f_add_column(home team score). The value: 4 | 2 | 1 | 1 | 2 | 3 | 1 | 0\n\nStep 2: Filter out useless columns.\nsimilar words of the question link to columns :\nscore -> home team score\ncolumn value of the question link to columns :\nNone\nsemantic sentence of the question link to columns :\nNone\nSo we use f_select_column(home team score).\n\nStep 3: After using f_add_column(home team score) and f_select_column(home team score), we obtain the sub table:\n/*\ncol   :  home team score\nrow 1 :  4\nrow 2 :  2\nrow 3 :  1\nrow 4 :  1\nrow 5 :  2\nrow 6 :  3\nrow 7 :  1\nrow 8 :  0\n*/\nThe average score of all home team members for all dates can be calculated by adding all the scores together and dividing by the number of rows. The sum of all scores is 17 (4+2+1+1+2+3+1+0) and there are 8 rows. Therefore, the average score is 2.125.\n\nPrediction Answer:\nYES\n\nCritique:\nStep 1 makes a correct attempt at extracting the home team score from the given \"score\" column. By creating a new column and populating it with the appropriate values based on the format of the scores provided in the original table, it sets up the data in a way that can be used for further calculation related to the home team scores. Step 1 is correct.\nStep 2 effectively filters the columns to focus only on the newly created \"home team score\" column, which is the relevant data needed to calculate the average score of the home team members as asked in the question. This step is a proper way to narrow down the data for the subsequent calculation step. Step 2 is correct.\nStep 3 has a calculation error. When adding up the scores (4 + 2 + 1 + 1 + 2 + 3 + 1 + 0), the sum is indeed 14, not 17 as stated. Step 3 is incorrect.\n\nConclusion: [Incorrect] Step 3",
\t"Original Table:\n/*\ncol   : tie | home team              | score | away team          | attendance\nrow 1 : 1   | aylesbury united       | 2-2   | windsor & eton     | 847\nrow 2 : 2   | burscough              | 5-0   | wakefield & emley  | 437\nrow 3 : 3   | dover athletic         | 0-3   | forest green roves | 932\nrow 4 : 4   | farnborough town       | 2-0   | halifax town       | 863\nrow 5 : 5   | gloucester city        | 1-1   | southport          | 1,237\nrow 6 : 6   | havant & waterlooville | 3-0   | hayes              | 456\nrow 7 : 7   | margate                | 0-2   | tamworth           | 971\nrow 8 : 8   | yeovil town            | 2-1   | northwich victoria | 4,469\n*/\n\nStatement:\n6 games attendance was under 1000\n\nReasoning Steps:\nStep 1: Select relevant rows. \nThe question aims to find out how many games had an attendance of less than 1000 people. To answer this, we need to count the number of rows where the attendance column shows a number less than 1000. So we use f_select_row(row 1, row 2, row 3, row 4, row 6, row 7).\n\nStep 2: Filter out useless columns.\nsimilar words of the question link to columns :\nunder 1000 -> attendance\ncolumn value of the question link to columns :\n1000 -> attendance\nsemantic sentence of the question link to columns :\nNone\nSo we use f_select_column(attendance).\n\nStep 3: After using f_select_row(row 1, row 2, row 3, row 4, row 6, row 7) and f_select_column(attendance), we obtain the sub table:\n/*\ncol   : attendance\nrow 1 : 847\nrow 2 : 437\nrow 3 : 932\nrow 4 : 863\nrow 5 : 456\nrow 6 : 971\n*/\nThe games with attendance under 1000 were rows 1, 2, 4, and 5. Therefore, there were 4 games with attendance under 1000.\n\nPrediction Answer:\nNO\n\nCritique:\nStep 1 correctly selects the rows that are relevant for further analysis regarding the attendance being under 1000. It includes all the rows where the attendance values might potentially be less than 1000, which are row 1, row 2, row 3, row 4, row 6, and row 7. This step makes the proper initial identification based on the condition stated in the question. Step 1 is correct.\nStep 2 filters out the columns effectively by choosing the \"attendance\" column. Since the question is focused on the attendance values to determine which are under 1000, this step narrows down the data to just what's needed for the subsequent steps. Step 2 is correct.\nStep 3 makes an error in counting the number of games with attendance under 1000. Looking at the sub-table from Step 3, all the rows shown (row 1 with 847, row 2 with 437, row 3 with 932, row 4 with 863, row 5 with 456, row 6 with 971) have attendance values that are less than 1000. Step 3 is incorrect.\n\nConclusion: [Incorrect] Step 3"
]
List 2: [
\t"Original Table:\n/*\ncol   : week | date    | opponent                     | score | result | record\nrow 1 : 1    | july 9  | vs. saskatchewan roughriders | 31\u201321 | win    | 1\u20130\nrow 2 : 2    | july 24 | vs. hamilton tiger-cats      | 36\u201325 | loss   | 2\u20131\nrow 3 : 3    | aug 1   | at edmonton eskimos          | 32\u201326 | win    | 3\u20131\nrow 4 : 4    | aug 8   | vs. bc lions                 | 29\u201316 | win    | 4\u20131\nrow 5 : 5    | aug 20  | at calgary stampeders        | 35\u20134  | win    | 5\u20131\nrow 6 : 6    | sept 11 | vs. calgary stampeders       | 15\u201311 | loss   | 7\u20132\nrow 7 : 7   | sept 18 | at ottawa rough riders       | 38\u201328 | loss   | 7\u20133\nrow 8 : 8   | sept 25 | vs. montreal concordes       | 19\u201316 | win    | 8\u20133\nrow 9 : 9   | oct 2   | at bc lions                  | 29\u201319 | win    | 9\u20133\nrow 10 : 10   | oct 23  | vs. edmonton eskimos         | 33\u201317 | loss   | 11\u20134\nrow 11 : 11   | nov 7   | at hamilton tiger-cats       | 24\u201321 | loss   | 11\u20135\n*/\n\nStatement:\nthe average number of points scored by opponents in the five games lost this season is 29.2\n\nReasoning Steps:\nStep 1: Select relevant rows. \nThe question aims to calculate the average number of points scored by opponents in the games that were lost during the season. We need to identify the rows representing the games that ended in a loss, note the scores of the opponents in those games, and then calculate the average of those scores. So we use f_select_row(row 2, row 6, row 7, row 10, row 11).\n\nStep 2: Filter out useless columns.\nsimilar words of the question link to columns :\nthe average number of points scored -> score\nby opponents -> opponent\nin the five games lost -> result\ncolumn value of the question link to columns :\nloss -> result\nsemantic sentence of the question link to columns :\nwhat is the average number of points scored by opponents in the five games lost -> opponent, score\nSo we use f_select_column(opponent, score, result).\n\nStep 3: After using f_select_row(row 2, row 6, row 7, row 10, row 11) and f_select_column(opponent, score, result), we obtain the sub table:\n/*\ncol   : opponent                | score | result\nrow 1 : vs. hamilton tiger-cats | 36\u201325 | loss\nrow 2 : vs. calgary stampeders  | 15\u201311 | loss\nrow 3 : at ottawa rough riders  | 38\u201328 | loss\nrow 4 : vs. edmonton eskimos    | 33\u201317 | loss\nrow 5 : at hamilton tiger-cats  | 24\u201321 | loss\n*/\nThe scores for the opponents in the five lost games are as follows:\nHamilton Tiger-Cats: 36\nCalgary Stampeders: 15\nOttawa Rough Riders: 38\nEdmonton Eskimos: 33\nHamilton Tiger-Cats: 24\nBy adding these scores together and dividing by 5, we get the average number of points scored by opponents in the five games lost this season, which is 30.\n\nPrediction Answer:\nNO\n\nCritique:\nStep 1 correctly identifies the relevant rows which correspond to the games that were lost during the season. By looking at the 'result' column and selecting the rows where the result is 'loss', it picks out the appropriate data points for further analysis. Step 1 is correct.\nStep 2 filters the necessary columns (opponent, score, and result) to focus only on the information relevant to answering the question. This step is a valid approach as it narrows down the data to what is needed to calculate the average points scored by opponents in the lost games. Step 2 is correct.\nStep 3 correctly extracts the opponents' scores as 36 (from 36\u201325), 15 (from 15\u201311), 38 (from 38\u201328), 33 (from 33\u201317), and 24 (from 24\u201321). But there was a miscalculation either in adding the scores together or in the division to find the average. Step 3 is incorrect.\n\nConclusion: [Incorrect] Step 3"
]

Explanation:
The errors in both lists are fundamentally about reasoning mistakes tied to the final query.
Splitting the lists into separate subcategories is unnecessary, as they align well under the overarching theme of "final query error."

Determination:
List 1: <final query error>
List 2: <final query error>


Example 3:
Parent Category: final query error

List 1: [
\t"Original Table:\n/*\ncol   : date             | home team         | score | away team       | notes\nrow 1 : 17 december 2007 | foolad            | 4-4   | esteghlal ahvaz | foolad progress 8-7 on penalties\nrow 2 : 21 december 2007 | rah ahan          | 2-2   | steel azin      | rah ahan progress 5-2 on penalties\nrow 3 : 21 december 2007 | zob ahan          | 1-1   | esteghlal       | esteghlal progress 3-1 on penalties\nrow 4 : 21 december 2007 | bargh shiraz      | 1-0   | paykan tehran\nrow 5 : 21 december 2007 | shahin bushehr    | 2-2   | saba battery    | shahin bushehr progress 6-5 on penalties\nrow 6 : 24 december 2007 | pas hamedan       | 3-0   | persepolis\nrow 7 : 26 february 2008 | moghavemat sepasi | 1-2   | sepahan\nrow 8 : 4 march 2008     | sanaye arak       | 0-1   | pegah gilan\n*/\n\n\nStatement:\nthe average score of all home team members for all dates is 2.125\n\nReasoning Steps:\nStep 1: Add necessary columns to the table.\nThe question asks about the average score of all home team members for all dates. We need to know the score of each match, which is given in the \"score\" column. The scores are in the format home-team-score-away-team-score. We extract the home team score for each row and create a different column \"home team score\" for each row. The datatype is numerical. So we use f_add_column(home team score). The value: 4 | 2 | 1 | 1 | 2 | 3 | 1 | 0\n\nStep 2: Filter out useless columns.\nsimilar words of the question link to columns :\nscore -> home team score\ncolumn value of the question link to columns :\nNone\nsemantic sentence of the question link to columns :\nNone\nSo we use f_select_column(home team score).\n\nStep 3: After using f_add_column(home team score) and f_select_column(home team score), we obtain the sub table:\n/*\ncol   :  home team score\nrow 1 :  4\nrow 2 :  2\nrow 3 :  1\nrow 4 :  1\nrow 5 :  2\nrow 6 :  3\nrow 7 :  1\nrow 8 :  0\n*/\nThe average score of all home team members for all dates can be calculated by adding all the scores together and dividing by the number of rows. The sum of all scores is 17 (4+2+1+1+2+3+1+0) and there are 8 rows. Therefore, the average score is 2.125.\n\nPrediction Answer:\nYES\n\nCritique:\nStep 1 makes a correct attempt at extracting the home team score from the given \"score\" column. By creating a new column and populating it with the appropriate values based on the format of the scores provided in the original table, it sets up the data in a way that can be used for further calculation related to the home team scores. Step 1 is correct.\nStep 2 effectively filters the columns to focus only on the newly created \"home team score\" column, which is the relevant data needed to calculate the average score of the home team members as asked in the question. This step is a proper way to narrow down the data for the subsequent calculation step. Step 2 is correct.\nStep 3 has a calculation error. When adding up the scores (4 + 2 + 1 + 1 + 2 + 3 + 1 + 0), the sum is indeed 14, not 17 as stated. Step 3 is incorrect.\n\nConclusion: [Incorrect] Step 3",
\t"Original Table:\n/*\ncol   : week | date    | opponent                     | score | result | record\nrow 1 : 1    | july 9  | vs. saskatchewan roughriders | 31\u201321 | win    | 1\u20130\nrow 2 : 2    | july 24 | vs. hamilton tiger-cats      | 36\u201325 | loss   | 2\u20131\nrow 3 : 3    | aug 1   | at edmonton eskimos          | 32\u201326 | win    | 3\u20131\nrow 4 : 4    | aug 8   | vs. bc lions                 | 29\u201316 | win    | 4\u20131\nrow 5 : 5    | aug 20  | at calgary stampeders        | 35\u20134  | win    | 5\u20131\nrow 6 : 6    | sept 11 | vs. calgary stampeders       | 15\u201311 | loss   | 7\u20132\nrow 7 : 7   | sept 18 | at ottawa rough riders       | 38\u201328 | loss   | 7\u20133\nrow 8 : 8   | sept 25 | vs. montreal concordes       | 19\u201316 | win    | 8\u20133\nrow 9 : 9   | oct 2   | at bc lions                  | 29\u201319 | win    | 9\u20133\nrow 10 : 10   | oct 23  | vs. edmonton eskimos         | 33\u201317 | loss   | 11\u20134\nrow 11 : 11   | nov 7   | at hamilton tiger-cats       | 24\u201321 | loss   | 11\u20135\n*/\n\nStatement:\nthe average number of points scored by opponents in the five games lost this season is 29.2\n\nReasoning Steps:\nStep 1: Select relevant rows. \nThe question aims to calculate the average number of points scored by opponents in the games that were lost during the season. We need to identify the rows representing the games that ended in a loss, note the scores of the opponents in those games, and then calculate the average of those scores. So we use f_select_row(row 2, row 6, row 7, row 10, row 11).\n\nStep 2: Filter out useless columns.\nsimilar words of the question link to columns :\nthe average number of points scored -> score\nby opponents -> opponent\nin the five games lost -> result\ncolumn value of the question link to columns :\nloss -> result\nsemantic sentence of the question link to columns :\nwhat is the average number of points scored by opponents in the five games lost -> opponent, score\nSo we use f_select_column(opponent, score, result).\n\nStep 3: After using f_select_row(row 2, row 6, row 7, row 10, row 11) and f_select_column(opponent, score, result), we obtain the sub table:\n/*\ncol   : opponent                | score | result\nrow 1 : vs. hamilton tiger-cats | 36\u201325 | loss\nrow 2 : vs. calgary stampeders  | 15\u201311 | loss\nrow 3 : at ottawa rough riders  | 38\u201328 | loss\nrow 4 : vs. edmonton eskimos    | 33\u201317 | loss\nrow 5 : at hamilton tiger-cats  | 24\u201321 | loss\n*/\nThe scores for the opponents in the five lost games are as follows:\nHamilton Tiger-Cats: 36\nCalgary Stampeders: 15\nOttawa Rough Riders: 38\nEdmonton Eskimos: 33\nHamilton Tiger-Cats: 24\nBy adding these scores together and dividing by 5, we get the average number of points scored by opponents in the five games lost this season, which is 30.\n\nPrediction Answer:\nNO\n\nCritique:\nStep 1 correctly identifies the relevant rows which correspond to the games that were lost during the season. By looking at the 'result' column and selecting the rows where the result is 'loss', it picks out the appropriate data points for further analysis. Step 1 is correct.\nStep 2 filters the necessary columns (opponent, score, and result) to focus only on the information relevant to answering the question. This step is a valid approach as it narrows down the data to what is needed to calculate the average points scored by opponents in the lost games. Step 2 is correct.\nStep 3 correctly extracts the opponents' scores as 36 (from 36\u201325), 15 (from 15\u201311), 38 (from 38\u201328), 33 (from 33\u201317), and 24 (from 24\u201321). But there was a miscalculation either in adding the scores together or in the division to find the average. Step 3 is incorrect.\n\nConclusion: [Incorrect] Step 3"
]
List 2: [
\t"Original Table:\n/*\ncol   : tie | home team              | score | away team          | attendance\nrow 1 : 1   | aylesbury united       | 2-2   | windsor & eton     | 847\nrow 2 : 2   | burscough              | 5-0   | wakefield & emley  | 437\nrow 3 : 3   | dover athletic         | 0-3   | forest green roves | 932\nrow 4 : 4   | farnborough town       | 2-0   | halifax town       | 863\nrow 5 : 5   | gloucester city        | 1-1   | southport          | 1,237\nrow 6 : 6   | havant & waterlooville | 3-0   | hayes              | 456\nrow 7 : 7   | margate                | 0-2   | tamworth           | 971\nrow 8 : 8   | yeovil town            | 2-1   | northwich victoria | 4,469\n*/\n\nStatement:\n6 games attendance was under 1000\n\nReasoning Steps:\nStep 1: Select relevant rows. \nThe question aims to find out how many games had an attendance of less than 1000 people. To answer this, we need to count the number of rows where the attendance column shows a number less than 1000. So we use f_select_row(row 1, row 2, row 3, row 4, row 6, row 7).\n\nStep 2: Filter out useless columns.\nsimilar words of the question link to columns :\nunder 1000 -> attendance\ncolumn value of the question link to columns :\n1000 -> attendance\nsemantic sentence of the question link to columns :\nNone\nSo we use f_select_column(attendance).\n\nStep 3: After using f_select_row(row 1, row 2, row 3, row 4, row 6, row 7) and f_select_column(attendance), we obtain the sub table:\n/*\ncol   : attendance\nrow 1 : 847\nrow 2 : 437\nrow 3 : 932\nrow 4 : 863\nrow 5 : 456\nrow 6 : 971\n*/\nThe games with attendance under 1000 were rows 1, 2, 4, and 5. Therefore, there were 4 games with attendance under 1000.\n\nPrediction Answer:\nNO\n\nCritique:\nStep 1 correctly selects the rows that are relevant for further analysis regarding the attendance being under 1000. It includes all the rows where the attendance values might potentially be less than 1000, which are row 1, row 2, row 3, row 4, row 6, and row 7. This step makes the proper initial identification based on the condition stated in the question. Step 1 is correct.\nStep 2 filters out the columns effectively by choosing the \"attendance\" column. Since the question is focused on the attendance values to determine which are under 1000, this step narrows down the data to just what's needed for the subsequent steps. Step 2 is correct.\nStep 3 makes an error in counting the number of games with attendance under 1000. Looking at the sub-table from Step 3, all the rows shown (row 1 with 847, row 2 with 437, row 3 with 932, row 4 with 863, row 5 with 456, row 6 with 971) have attendance values that are less than 1000. Step 3 is incorrect.\n\nConclusion: [Incorrect] Step 3"
]

Explanation:
The examples can be divided into two subcategories: calculation error and logical error, based on the nature of the mistakes. Calculation errors occur when the reasoning steps and data selection are correct, but numerical operations, such as addition or averaging, are performed incorrectly, as seen in List 1 examples. Logical errors arise from flawed reasoning, such as incorrect row or column selection or misinterpretation of conditions, as demonstrated in List 2 examples. This division provides clarity by distinguishing errors stemming from arithmetic mistakes from those caused by faulty reasoning or data interpretation.

Determination:
List 1: <calculation error>
List 2: <logical error>


Example 4:
Parent Category: row error

List 1: [
\t"Original Table:\n/*\ncol   : goal | date         | location          | opponent | lineup              | min | assist/pass | score | result | competition\nrow 1 : 1    | may 9, 2004  | usaalbuquerque nm | mexico   | on 70' (off lilly)  | 19  | tarpley     | 3\u20130   | 3\u20130    | friendly\nrow 2 : 2    | jun 26, 2005 | usavirginia beach | canada   | 90.start            | 12  | unassisted  | 1\u20130   | 2\u20130    | friendly\nrow 3 : 3    | jan 30, 2007 | chnguangzhou      | china pr | 90.start            | 46+ | unassisted  | 1\u20130   | 2\u20130    | four nations tournament\nrow 4 : 4    | may 12, 2007 | usafrisco tx      | canada   | off 72' (on wagner) | 28  | tarpley     | 3\u20131   | 6\u20132    | friendly\nrow 5 : 5    | sep 18, 2007 | chnshanghai       | nigeria  | 90.start            | 1   | wambach     | 1\u20130   | 1\u20130    | world cup \u2013 group b\nrow 6 : 6    | sep 30, 2007 | chnshanghai       | norway   | 90.start            | 58  | unassisted  | 3\u20130   | 4\u20131    | world cup final - third place playoff\nrow 7 : 7    | aug 18, 2008 | chnbeijing        | japan    | 90.start            | 44  | rodriguez   | 2\u20131   | 4\u20132    | olympics tournament\nrow 8 : 8    | sep 20, 2008 | usabridgeview il  | ireland  | 90.start            | 19  | tarpley     | 1\u20130   | 2\u20130    | friendly\n*/\n\nStatement:\nchalupny scored in 4 consecutive friendly competitions\n\nReasoning Steps:\nStep 1: Select relevant rows.\nThe question aims to find out the number of consecutive friendly competitions in which Chalupny scored. We need to look at the rows where the competition type is \"friendly\" and check the dates to determine if they are consecutive. The relevant rows are row 1, row 2, and row 4. So we use f_select_row(row 1, row 2, row 4).\n\nStep 2: Filter out useless columns.\nsimilar words of the question link to columns :\nscored in -> goal\nconsecutive -> date\nfriendly competitions -> competition\ncolumn value link to columns :\nfriendly -> competition\nSo we use f_select_column(goal, date, competition).\n  \nStep 3: Group the column of competition. So we use f_group_column(competition).\n\nStep 4: After using f_select_row(row 1, row 2, row 4), f_select_column(goal, date, competition) and f_group_column(competition), we obtain the sub table:\n/*\ncol : goal |       date  | competition\nrow 1 : 1 | may 9, 2004 | friendly\nrow 2 : 2 | jun 26, 2005 | friendly\nrow 3 : 4 | may 12, 2007 | friendly\n*/\n/*\nGroup the rows according to column: competition.\nGroup ID | competition | Count\nGroup 1 | friendly | 3\n*/\nChalupny did not score in any consecutive friendly competitions. The gaps in dates between her goals indicate non-consecutive friendly matches.\n\nPrediction Answer:\nNO\n\nCritique:\nRow 8 was omitted in Step 1, despite satisfying the criteria. The reasoning only considers rows 1, 2, and 4, which makes Step 1 incomplete and therefore incorrect. Step 1 is incorrect.\n\nConclusion: [Incorrect] Step 1",
\t"Original Table:\n/*\ncol   : club                                | founded | nickname  | location           | home ground                  | entered competition | most recent promotion\nrow 1 : bundoora football club              | 1974    | bulls     | bundoora           | yulong reserve               | 1981                | 1982\nrow 2 : eltham football club                | 1909    | panthers  | eltham             | central park                 | 1922                | 2003\nrow 3 : greensborough football club         | 1905    | boro      | greensborough      | war memorial park            | 1922                | 2007\nrow 4 : heidelberg football club            | 1876    | tigers    | heidelberg         | warringal park               | 1923                | 1983\nrow 5 : lalor football club                 | 1955    | bloods    | lalor              | lalor reserve                | 1968                | 2011\nrow 6 : macleod football club               | 1946    | kangaroos | rosanna            | de winton park               | 1947                | 2010\nrow 7 : montmorency football club           | 1924    | magpies   | montmorency        | montmorency park, north oval | 1924                | n/a\nrow 8 : north heidelberg football club      | 1958    | bulldogs  | heidelberg heights | shelley street reserve       | 1958                | n/a\nrow 9 : northcote park football club        | 1952    | cougars   | northcote          | bill lawry oval              | 1982                | 1995\nrow 10 : west preston lakeside football club | 1998    | roosters  | reservoir          | j e moore park               | 1996                | 1997\n*/\n\nStatement:\nthere are 5 division 1 teams that were founded before 1950\n\nReasoning Steps:\nStep 1: Select relevant rows. \nThe question aims to find out the number of Division 1 teams that were founded before the year 1950. We need to look at the \"founded\" column and count the number of teams that meet this criterion. So we use f_select_row(row 2, row 3, row 4, row 8).\n\nStep 2: Filter out useless columns.\nsimilar words of the question link to columns :\ndivision 1 teams -> club\nfounded before 1950 -> found\ncolumn value of the question link to columns :\n1950 -> found\nsemantic sentence of the question link to columns :\nNone\nSo we use f_select_column(club, found).\n\nStep 3: After using f_select_row(row 2, row 3, row 4, row 8) and f_select_column(club, found), we obtain the sub table:\n/*\ncol   : club                            | founded\nrow 1 : eltham football club            | 1909\nrow 2 : greensborough football club     | 1905\nrow 3 : heidelberg football club        | 1876\nrow 4 : north heidelberg football club  | 1958\n*/\nThe clubs founded before 1950 that are in Division 1 are Eltham Football Club, Greensborough Football Club, and Heidelberg Football Club.\n\nPrediction Answer:\nNO\n\nCritique:\nStep 1 is incorrect as it misses some of the relevant rows. While it correctly includes row 2, row 3, and row 4, it wrongly includes row 8 which was founded in 1958 and thus doesn't meet the \"founded before 1950\" criterion. Additionally, it fails to include other rows like row 6 (founded in 1946) and row 7 (founded in 1924) as it meets the condition of being founded before 1950. This step is flawed in its selection of rows and thus incorrect. Step 1 is incorrect.\n\nConclusion: [Incorrect] Step 1"
]
List 2: [
\t"Original Table:\n/*\ncol   : club                     | league              | sport             | venue                               | established | championships\nrow 1 : madison mustangs         | ifl                 | american football | breitenbach stadium                 | 1997        | 4 consecutive ironbowls\nrow 2 : madison mallards         | nl                  | baseball          | warner park                         | 2001        | 1 championship\nrow 3 : madison 56ers            | npsl                | soccer            | breese stevens field                | 2005        | 0 championships\nrow 4 : wisconsin rugby club     | wrfu                | rugby             | wisconsin rugby club sports complex | 1962        | 2 championships\nrow 5 : madison minotaurs        | wrfu                | rugby             | yahara rugby field                  | 2007        | 0 bingham cups\nrow 6 : wisconsin badgers        | big ten, ncaa div.1 | 23 varsity teams  | camp randall stadium, kohl center   | 1849        | 27 championships\nrow 7 : edgewood eagles          | nacc, ncaa div.3    | 16 varsity teams  | edgedome                            | 1974        | 35 championships\nrow 8 : madison college wolfpack | n4c, njcaa div.3    | 8 varsity teams   | redsten gymnasium, roberts field    | 1912        | 21 championships\nrow 9 : mad rollin' dolls        | wftda               | roller derby      | alliant energy center               | 2005        | 0 championships\nrow 10 : madison blues            | glhl                | hockey            | capitol ice arena                   | 2010        | 0 championships\n*/\n\nStatement:\nthere are 3 current teams that have been in existence for 25 years or greater\n\nReasoning Steps:\nStep 1: Select relevant rows.\nThe question aims to identify the number of teams that have existed for 25 years or more. We need to look at the \"established\" column and filter the rows based on the year being 1998 or earlier.\nSo we use f_select_row(row 1, row 4, row 6, row 8).\n\nStep 2: Filter out useless columns.\nsimilar words of the question link to columns:\nhow many current teams -> club\nhave been in existence -> established\nfor 25 years or greater -> established\ncolumn value of the question link to columns:\n25 years or greater -> established\nsemantic sentence of the question link to columns:\nNone\nSo we use f_select_column(club, established).\n\nStep 3: After using f_select_row(row 1, row 4, row 6, row 8) and f_select_column(club, established), we obtain the sub table:\n/*\ncol   : club                     | established\nrow 1 : madison mustangs         | 1997\nrow 2 : wisconsin rugby club     | 1962\nrow 3 : wisconsin badgers        | 1849\nrow 4 : madison college wolfpack | 1912\n*/\nThe Wisconsin Rugby Club was established in 1962, the Wisconsin Badgers in 1849, and the Madison College Wolfpack in 1912. All of these clubs have been in existence for more than 25 years. The Madison Mustangs were established in 1997, which is less than 25 years from the current year (assuming the current year is 2023). Therefore, the number of current teams that have been in existence for 25 years or greater is 3.\n\nPrediction Answer:\nYES\n\nCritique:\nStep 1 partially identifies the relevant rows that have existed for 25 years or more. The selected rows (row 4, row 6, row 8) are based on the \"established\" year being 1998 or earlier. However, this step incorrectly includes row 1 as relevant and misses row 7 (Edgewood Eagles, established in 1974), which also meets the criteria. This misjudgment and omission render Step 1 incomplete and incorrect.\n\nConclusion: [Incorrect] Step 1"
]

Explanation:
Both lists should remain under the parent category "row error" as they focus on reasoning mistakes involving incorrect row selection, such as the omission of relevant rows or the inclusion of irrelevant ones. In List 1, errors include failing to select rows that meet specific conditions, such as omitting a "friendly competition" row or missing rows founded before 1950. Similarly, List 2 demonstrates misjudgments in row selection, such as including rows that do not meet the criteria of being established for over 25 years while omitting valid ones. Since both lists exhibit consistent row selection errors, they align well under the shared category of "row error" without the need for further subdivision.

Determination:
List 1: <row error>
List 2: <row error>


"""

horizontal_expansion_few_shot = """You are given an error tree represented as a dictionary and a template describing a specific error. If the error path corresponding to the template cannot be found in the error tree, extend the error tree by adding a new branch at the appropriate location. Ensure that:
    - The new branch aligns logically with the existing structure of the error tree.
    - The template can be correctly integrated into the tree under the newly added branch.

Here are some examples:
Example 1:
Error Tree:
{
    "sub-table error": {
        "row error": "<END>",
        "column error": "<END>"
    }
}

Template:
Original Table:\n/*\ncol   : tie | home team              | score | away team          | attendance\nrow 1 : 1   | aylesbury united       | 2-2   | windsor & eton     | 847\nrow 2 : 2   | burscough              | 5-0   | wakefield & emley  | 437\nrow 3 : 3   | dover athletic         | 0-3   | forest green roves | 932\nrow 4 : 4   | farnborough town       | 2-0   | halifax town       | 863\nrow 5 : 5   | gloucester city        | 1-1   | southport          | 1,237\nrow 6 : 6   | havant & waterlooville | 3-0   | hayes              | 456\nrow 7 : 7   | margate                | 0-2   | tamworth           | 971\nrow 8 : 8   | yeovil town            | 2-1   | northwich victoria | 4,469\n*/\n\nStatement:\n6 games attendance was under 1000\n\nReasoning Steps:\nStep 1: Select relevant rows. \nThe question aims to find out how many games had an attendance of less than 1000 people. To answer this, we need to count the number of rows where the attendance column shows a number less than 1000. So we use f_select_row(row 1, row 2, row 3, row 4, row 6, row 7).\n\nStep 2: Filter out useless columns.\nsimilar words of the question link to columns :\nunder 1000 -> attendance\ncolumn value of the question link to columns :\n1000 -> attendance\nsemantic sentence of the question link to columns :\nNone\nSo we use f_select_column(attendance).\n\nStep 3: After using f_select_row(row 1, row 2, row 3, row 4, row 6, row 7) and f_select_column(attendance), we obtain the sub table:\n/*\ncol   : attendance\nrow 1 : 847\nrow 2 : 437\nrow 3 : 932\nrow 4 : 863\nrow 5 : 456\nrow 6 : 971\n*/\nThe games with attendance under 1000 were rows 1, 2, 4, and 5. Therefore, there were 4 games with attendance under 1000.\n\nPrediction Answer:\nNO\n\nCritique:\nStep 1 correctly selects the rows that are relevant for further analysis regarding the attendance being under 1000. It includes all the rows where the attendance values might potentially be less than 1000, which are row 1, row 2, row 3, row 4, row 6, and row 7. This step makes the proper initial identification based on the condition stated in the question. Step 1 is correct.\nStep 2 filters out the columns effectively by choosing the \"attendance\" column. Since the question is focused on the attendance values to determine which are under 1000, this step narrows down the data to just what's needed for the subsequent steps. Step 2 is correct.\nStep 3 makes an error in counting the number of games with attendance under 1000. Looking at the sub-table from Step 3, all the rows shown (row 1 with 847, row 2 with 437, row 3 with 932, row 4 with 863, row 5 with 456, row 6 with 971) have attendance values that are less than 1000. Step 3 is incorrect.\n\nConclusion: [Incorrect] Step 3

Explanation:
The error identified in the template corresponds to an issue in the final reasoning step, specifically during the conclusion stage. To accommodate this error logically in the error tree, the branch "final query error" was added. This branch categorizes mistakes that occur when arriving at the final prediction or conclusion, ensuring the tree structure remains comprehensive and adaptable to similar issues in the future.

Addition: (final query error -> <END>)


Example 2:
Error Tree:
{
    "sub-table error": {
        "row misidentification error": "<END>",
        "row omission error": "<END>"
    },
    "final query error": "<END>"
}

Template:
Original Table:\n/*\ncol   : res. | record | opponent         | method                        | event                                        | date               | round | time | location                                | notes\nrow 1 : win  | 12-3   | mike hayes       | ko (punch)                    | ksw 25: khalidov vs. sakurai                 | december 7, 2013   | 1     | 1:12 | wroc\u0142aw, poland\nrow 2 : win  | 11\u20133   | nick moghadden   | tko (punches)                 | bellator 99                                  | september 13, 2013 | 1     | 3:22 | temecula, california, united states     | bellator debut\nrow 3 : loss | 10\u20133   | guto inocente    | decision (unanimous)          | strikeforce: barnett vs. cormier             | may 19, 2012       | 3     | 5:00 | san jose, california, united states     | light heavyweight debut\nrow 4 : win  | 10\u20132   | brett albee      | tko (strikes)                 | strikeforce: diaz vs. daley                  | april 9, 2011      | 1     | 1:46 | san diego, california, united states\nrow 5 : loss | 9\u20132    | lavar johnson    | ko (punches)                  | strikeforce challengers: bowling vs. voelker | october 22, 2010   | 1     | 2:17 | fresno, california, united states\nrow 6 : win  | 9\u20131    | eddie sapp       | submission (rear-naked choke) | native fighting championship 6               | august 14, 2010    | 1     | 2:01 | campo, california, united states\nrow 7 : loss | 8\u20131    | cody goodale     | decision (unanimous)          | gladiator challenge: maximum force           | april 25, 2010     | 3     | 5:00 | san jacinto, california, united states\n*/\n\nStatement:\nvirgil zwicker had 6 losses.\n\nReasoning Steps:\nStep 1: Select relevant rows.\nThe question aims to find out the number of losses Virgil Zwicker had based on the provided fight records. We need to count the rows where the \"res.\" column shows \"loss\".\nSo we use f_select_row(row 3, row 5, row 7).\n\nStep 2: Filter out useless columns.\nsimilar words of the question link to columns:\nloses -> record\ncolumn value of the question link to columns:\n10\u20133 -> record\nsemantic sentence of the question link to columns:\nNone\nSo we use f_select_column(record).\n\nStep 3: After using f_select_row(row 3, row 5, row 7) and f_select_column(record), we obtain the sub table:\n/*\ncol   : record\nrow 1 : 10\u20133\nrow 2 : 9\u20132\nrow 3 : 8\u20131\n*/\nThe provided table shows records of wins and losses but does not specify who the records belong to. However, if we assume that the table represents Virgil Zwicker's records, then we can deduce the number of losses from each record. The losses in the records are 3, 2, and 1 respectively. If we consider each row as a separate season or period, then the total number of losses would be the sum of these losses: 3 + 2 + 1 = 6.\n\nPrediction Answer:\nYES\n\nCritique:\nStep 1 correctly identifies the relevant rows where the \"res.\" column indicates a loss. The rows selected are indeed the ones where the outcome is a loss. Step 1 is correct.\nStep 2 incorrectly filters out the columns. The question asks for the number of losses, but the filtering step selects only the 'record' column, which combines wins and losses in a single string (e.g., \"10\u20133\"). This does not directly provide the number of losses. Instead, the 'res.' column should be used to count the losses directly. Step 2 is incorrect.\n\nConclusion: [Incorrect] Step 2

Explanation:
The error in the template occurs during Step 2, where the incorrect column ("record") is selected instead of the correct column ("res.") to count losses. This mistake falls under the category of column selection errors within the sub-table error context.
To address this, the error tree has to be updated by adding a new branch:
sub-table error -> column error -> <END>
Addition: (sub-table error -> column error -> <END>)

Example 3:
Error Tree:
{
    "sub-table error": {
        "column misidentification error": "<END>",
        "column omission error": "<END>"
    },
    "final query error": "<END>"
}

Template:
Original Table:\n/*\ncol   : goal | date         | location          | opponent | lineup              | min | assist/pass | score | result | competition\nrow 1 : 1    | may 9, 2004  | usaalbuquerque nm | mexico   | on 70' (off lilly)  | 19  | tarpley     | 3\u20130   | 3\u20130    | friendly\nrow 2 : 2    | jun 26, 2005 | usavirginia beach | canada   | 90.start            | 12  | unassisted  | 1\u20130   | 2\u20130    | friendly\nrow 3 : 3    | jan 30, 2007 | chnguangzhou      | china pr | 90.start            | 46+ | unassisted  | 1\u20130   | 2\u20130    | four nations tournament\nrow 4 : 4    | may 12, 2007 | usafrisco tx      | canada   | off 72' (on wagner) | 28  | tarpley     | 3\u20131   | 6\u20132    | friendly\nrow 5 : 5    | sep 18, 2007 | chnshanghai       | nigeria  | 90.start            | 1   | wambach     | 1\u20130   | 1\u20130    | world cup \u2013 group b\nrow 6 : 6    | sep 30, 2007 | chnshanghai       | norway   | 90.start            | 58  | unassisted  | 3\u20130   | 4\u20131    | world cup final - third place playoff\nrow 7 : 7    | aug 18, 2008 | chnbeijing        | japan    | 90.start            | 44  | rodriguez   | 2\u20131   | 4\u20132    | olympics tournament\nrow 8 : 8    | sep 20, 2008 | usabridgeview il  | ireland  | 90.start            | 19  | tarpley     | 1\u20130   | 2\u20130    | friendly\n*/\n\nStatement:\nchalupny scored in 4 consecutive friendly competitions\n\nReasoning Steps:\nStep 1: Select relevant rows.\nThe question aims to find out the number of consecutive friendly competitions in which Chalupny scored. We need to look at the rows where the competition type is \"friendly\" and check the dates to determine if they are consecutive. The relevant rows are row 1, row 2, and row 4. So we use f_select_row(row 1, row 2, row 4).\n\nStep 2: Filter out useless columns.\nsimilar words of the question link to columns :\nscored in -> goal\nconsecutive -> date\nfriendly competitions -> competition\ncolumn value link to columns :\nfriendly -> competition\nSo we use f_select_column(goal, date, competition).\n  \nStep 3: Group the column of competition. So we use f_group_column(competition).\n\nStep 4: After using f_select_row(row 1, row 2, row 4), f_select_column(goal, date, competition) and f_group_column(competition), we obtain the sub table:\n/*\ncol : goal |       date  | competition\nrow 1 : 1 | may 9, 2004 | friendly\nrow 2 : 2 | jun 26, 2005 | friendly\nrow 3 : 4 | may 12, 2007 | friendly\n*/\n/*\nGroup the rows according to column: competition.\nGroup ID | competition | Count\nGroup 1 | friendly | 3\n*/\nChalupny did not score in any consecutive friendly competitions. The gaps in dates between her goals indicate non-consecutive friendly matches.\n\nPrediction Answer:\nNO\n\nCritique:\nRow 8 was omitted in Step 1, despite satisfying the criteria. The reasoning only considers rows 1, 2, and 4, which makes Step 1 incomplete and therefore incorrect. Step 1 is incorrect.\n\nConclusion: [Incorrect] Step 1

Explanation:
The error in the template occurs during Step 1 when relevant rows (specifically Row 8) were omitted from the selection, making the row selection incomplete and incorrect. This type of mistake falls under the category of row errors within the sub-table error context.
To address this, the error tree has been updated with a new branch:
sub-table error -> row error -> <END>
This ensures that any issues related to row misidentification or omission are properly categorized, making the error tree more comprehensive and organized for handling similar issues in the future.
Addition: (sub-table error -> row error -> <END>)

"""

def format_list_to_string(lst):
    result = '[\n'
    for i in range(len(lst) - 1):
        result += f'\t{lst[i]},\n'
    result += f'\t{lst[-1]}\n'
    result += ']'
    return result

def vertical_expansion(few_shot, critic_template, error_type, parent_node, llm, llm_options):
    prompt = ""
    prompt += vertical_expansion_few_shot
    prompt += "Now, determine whether the two lists below can be meaningfully split into two distinct subcategories.\n"
    prompt += f"Parent Category: {error_type}\n\n"
    prompt += f"List 1: {format_list_to_string(random.sample(few_shot, min(5, len(few_shot))))}\n"
    prompt += f"List 2: {format_list_to_string([critic_template])}\n\n"
    prompt += "Explanation:\n"
    responses = llm.generate_plus_with_score(prompt, options=llm_options)
    names = re.findall(r'<(.*?)>', responses[0][0])
    if len(names) == 2 and names[0] != names[1]:
        parent_node[error_type] = {
            names[0]:few_shot,
            names[1]:[critic_template]
        }
    else:
        few_shot = few_shot.append(critic_template)

def horizontal_expansion(few_shot_dict, critic_template, llm, llm_options):
    prompt = ""
    prompt += horizontal_expansion_few_shot
    prompt += "Now, given the error tree and the template, if the error path corresponding to the template cannot be found in the error tree, extend the error tree by adding a new branch at the appropriate location.\n"
    modified_error_tree = replace_leaves_with_end(few_shot_dict)
    prompt += f"Error Tree:\n{modified_error_tree}\n\n"
    prompt += f"Template:\n{critic_template}\n\n"
    prompt += "Explanation:\n"
    responses = llm.generate_plus_with_score(prompt, options=llm_options)
    if "Addition" in responses[0][0]:
        route = re.findall(r'\((.*?)\)', responses[0][0].split("Addition:")[-1])
        if route:
            route = route[0]
        if '->' in route:
            route = route.split('->')
            few_shot = few_shot_dict
            for error_type in route:
                error_type = error_type.strip()
                if error_type in few_shot:
                    few_shot = few_shot[error_type]
                elif error_type != '<END>' and isinstance(few_shot, dict):
                    few_shot[error_type] = [critic_template]
                    break
                else:
                    break

def update_error_tree(sample, error_route, error_tree_json, llm, llm_options, lock):
    critic_template = ""
    critic_template += "Original Table:\n/*\n" + table2string(sample['table_text']) + "\n*/\n\n"
    critic_template += "Statement: \n" +  sample['statement'] + "\n\n"

    critic_template += "Reasoning Steps:\n"

    table_log, thought_log = get_table_log(sample)

    step = 0
    action_list = []
    table_text = sample['table_text']
    for idx, table_info in enumerate(table_log[:-1]):
        if table_info["act_chain"]:
            table_action = table_info["act_chain"][-1]
            if "skip" in table_action:
                continue
            else:
                table_text = table_info["table_text"]
                action_list.append(table_action)
                critic_template += f"Step{step+1}: {thought_log[idx]}\n"
                critic_template += f"So we use {table_action}.\n\n"
                step += 1


    if len(action_list):
        critic_template += f"Step{step+1}: After using "

        max_idx = len(action_list) - 1
        for idx, act in enumerate(action_list):
            critic_template += act
            if idx < max_idx-1:
                critic_template += ", "
            elif idx == max_idx-1:
                critic_template += " and "
        critic_template += ", we obtain the sub-table:\n/*\n"
        critic_template += f"{table2string(table_text)}\n*/\n"
        if "group_sub_table" in table_info:
            group_column, group_info = table_info["group_sub_table"]
            critic_template += "/*\n"
            critic_template += "Group the rows according to column: {}.\n".format(group_column)
            group_headers = ["Group ID", group_column, "Count"]
            group_rows = []
            for i, (v, count) in enumerate(group_info):
                if v.strip() == "":
                    v = "[Empty Cell]"
                group_rows.append([f"Group {i+1}", v, str(count)])
            critic_template += " | ".join(group_headers) + "\n"
            for row in group_rows:
                critic_template += " | ".join(row) + "\n"
            critic_template += "*/\n"
    
    critic_template += f"{thought_log[-1]}\n\n"

    critic_template += "Prediction Answer: \n" + table_log[-1]["cotable_result"].lower() + "\n\n"

    critic_template += "Critique:\n" + sample["critique"]  + "\n\n"

    critic_template += "Conclusion:\n" + sample["conclusion"]


    with lock:
        try:
            with open(error_tree_json, 'r') as f:
                few_shot_dict = json.load(f)

            if error_route != 'random':
                error_route = error_route.split('->')
                few_shot = few_shot_dict
                for error_type in error_route:
                    error_type = error_type.strip()
                    if error_type in few_shot:
                        parent_node = few_shot
                        few_shot = few_shot[error_type]
                        if isinstance(few_shot,list):
                            vertical_expansion(few_shot, critic_template, error_type, parent_node, llm=llm, llm_options=llm_options)
                            break
            else:
                horizontal_expansion(few_shot_dict, critic_template, llm, llm_options)
            ## 如果不是扩充template，就横向或纵向扩充分支
            
            with open(error_tree_json, 'w') as f:
                json.dump(few_shot_dict, f, indent=4)
        finally:
            pass