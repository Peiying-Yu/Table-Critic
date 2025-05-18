import json
correct_1 = ["""Original Table:
/*
col   : week | date    | opponent                     | score | result | record
row 1 : 1    | july 9  | vs. saskatchewan roughriders | 31–21 | win    | 1–0
row 2 : 2    | july 16 | at montreal concordes        | 36–0  | win    | 2–0
row 3 : 3    | july 24 | vs. hamilton tiger-cats      | 36–25 | loss   | 2–1
row 4 : 4    | aug 1   | at edmonton eskimos          | 32–26 | win    | 3–1
row 5 : 5    | aug 8   | vs. bc lions                 | 29–16 | win    | 4–1
row 6 : 6    | aug 20  | at calgary stampeders        | 35–4  | win    | 5–1
row 7 : 7   | sept 18 | at ottawa rough riders       | 38–28 | loss   | 7–3
row 8 : 8   | sept 25 | vs. montreal concordes       | 19–16 | win    | 8–3
row 9 : 9   | oct 2   | at bc lions                  | 29–19 | win    | 9–3
row 10 : 10   | oct 11  | vs. toronto argonauts        | 39–35 | win    | 10–3
*/

Question:
how many total points did the bombers score against the bc lions?

Reasoning Steps:
Step 1: Select relevant rows.
The question aims to find out the total points the Bombers scored against the BC Lions. We need to look at the rows where the opponent is the BC Lions and sum up the points scored by the Bombers in those games. The relevant rows are row 5 and row 9. So we use f_select_row(row 5, row 9).

Step 2: Filter out useless columns.
similar words of the question link to columns :
scored -> score
against -> opponent
column value of the question link to columns :
bc lions -> opponent
semantic sentence of the question link to columns :
the bombers scored -> score
So we use f_select_column(opponent, score).
 
Step 3: After using f_select_row(row 5, row 9) and f_select_column(opponent, score), we obtain the sub table:
/*
col   : opponent  score
row 1 : vs. bc lions  29–16
row 2 : at bc lions  29–19
*/
The Bombers scored 29 points in the first game and 29 points in the second game against the BC Lions. By adding these scores together, the total points scored by the Bombers against the BC Lions is 58.

Prediction Answer:
58

Analysis:
Step 1 correctly identifies the relevant rows where the opponent is the BC Lions: rows 5 and 9. The table clearly shows that in row 5, the Bombers scored 29 points, and in row 9, they also scored 29 points against the BC Lions. Step 1 is correct.
Step 2 filters the necessary columns (opponent and score) to focus only on the relevant information. Step 2 is correct.
Step 3 correctly adds the two scores: 29 + 29 = 58, which gives the correct total score. Step 3 is correct.

Conclusion: [Correct]"""]

correct_2 = ["""Original Table:
/*
col   : election | number of\npopular votes | % of\npopular votes | total\nelected seats | +/-
row 1 : 1988     | 139,982                  | 22.16               | 61 / 264
row 2 : 1991     | 170,757                  | 32.11               | 83 / 272             | 22
row 3 : 1994     | 242,557                  | 35.34               | 121 / 346            | 38
row 4 : 1999     | 271,251                  | 33.45               | 122 / 390            | 1
row 5 : 2003     | 459,640                  | 44.67               | 194 / 400            | 72
row 6 : 2007     | 445,781                  | 39.15               | 127 / 405            | 30
row 7 : 2011     | 464,512                  | 39.34               | 103 / 412            | 18
*/

Question:
which election was the first to reach over 40% of the popular vote?

Reasoning Steps:
Step 1: Select relevant rows.
The question aims to find out the first election in which the party reached over 40% of the popular vote. We need to look for the row where the percentage of popular votes is greater than 40% for the first time. So we use f_select_row(row 5).

Step 2: Filter out useless columns.
similar words of the question link to columns :
the election -> election
over 40% of the popular vote -> % of popular votes
column value of the question link to columns :
40% -> % of popular votes
semantic sentence of the question link to columns :
None
So we use f_select_column(election, % of popular votes).
 
Step 3: After using f_select_row(row 5) and f_select_column(election, % of popular votes), we obtain the sub table:
/*
col   : election | % of\npopular votes
row 1 : 2003     | 44.67               
*/
The election in row 1, which is the 2003 election, was the first to reach over 40% of the popular vote with 44.67%.

Prediction Answer:
2003

Analysis:
Step 1 correctly identifies row 5 as the relevant row since it is the first row where the percentage of popular votes exceeds 40%. The approach of looking for the first occurrence where the condition is met is logical. Step 1 is correct.
Step 2 filters the necessary columns (election and % of popular votes) to focus only on the relevant information for answering the question. This step is a valid way to narrow down the data to what is needed. Step 2 is correct.
Step 3 accurately interprets the remaining data in the sub-table and correctly determines that the 2003 election was the first to reach over 40% of the popular vote based on the value shown. Step 3 is correct.

Conclusion: [Correct]"""]

correct_3 = ["""Original Table:
/*
col   : institution            | location                      | enrollment | nickname      | varsity\nsports | rugby\nsince | head coach
row 1 : clemson university     | clemson, south carolina       | 20,576     | tigers        | 19              | 1967         | justin hickey
row 2 : maryland               | college park, maryland        | 37,641     | terrapins     | 20              | 1968         | jeff soeken
row 3 : navy                   | annapolis, maryland           | 4,576      | midshipmen    | 30              | 1963         | mike flanagan
row 4 : north carolina         | chapel hill, north carolina   | 29,340     | tar heels     | 28              | 1966         | pete earsman
row 5 : north carolina state   | raleigh, north carolina       | 34,767     | wolfpack      | 25              | 1965         | jim latham
row 6 : university of virginia | charlottesville, virginia     | 20,895     | cavaliers     | 25              | 1961         | jon roberts
row 7 : virginia tech          | blacksburg, virginia          | 30,379     | hokies        | 21              | 1891 / 1968  | andy richards
row 8 : wake forest            | winston-salem, north carolina | 7,079      | demon deacons | 18              | 1973         | patrick kane
*/

Question:
when was the first year of rugby of the terrapins?

Reasoning Steps:
Step 1: Select relevant rows.
The question aims to find out the first year of rugby for the Terrapins, which refers to the nickname of Maryland's sports teams. We need to look at the row that corresponds to Maryland to get the information regarding 'rugby since'. So we use f_select_row(row 2).

Step 2: Filter out useless columns.
similar words of the question link to columns :
the first year of rugby -> rugby\nsince
column value of the question link to columns :
terrapins -> nickname
semantic sentence of the question link to columns :
when was the first year of rugby of the terrapins? -> rugby\nsince
So we use f_select_column(nickname, rugby\nsince).

Step 3: After using f_select_row(row 2) and f_select_column(nickname, rugby\nsince), we obtain the sub table:
/*
col   : nickname   |  rugby\nsince
row 1 : terrapins   |    1963
*/
The first year of rugby for the Terrapins was 1963. 

Prediction Answer:
1963

Analysis:
Step 1 correctly identifies row 2 as the relevant row since the question is specifically asking about the Terrapins which is the nickname for the sports teams of Maryland. This step makes a proper selection based on the team in question. Step 1 is correct.
Step 2 filters the necessary columns (nickname and rugby\nsince) to focus only on the relevant information that will directly provide the answer regarding the first year of rugby for the Terrapins. This step is a valid approach to narrow down the data. Step 2 is correct.
Step 3 accurately interprets the remaining data in the sub-table and correctly determines that the first year of rugby for the Terrapins was 1963 based on the value shown. Step 3 is correct.

Conclusion: [Correct]"""]

correct_4 = ["""Original Table:
/*
col : event | performance | athlete | nation | place | date
row 1 : 100 m | 9.72 | usain bolt | jamaica | new york city ny, usa | may 31
row 2 : 100 m | 9.69 | usain bolt | jamaica | beijing, china | august 16
row 3 : 200 m | 19.30 | usain bolt | jamaica | beijing, china | august 20
row 4 : 4 x 100 m relay | 37.10 | nesta carter\nmichael frater\nusain bolt\nasafa powell | jamaica | beijing, china | august 22
row 5 : 110 m hurdles | 12.87 | dayron robles | cuba | ostrava, czech republic | june 12
row 6 : 50 km race walk | 3:34:14 | denis nizhegorodov | russia | cheboksary, russia | may 11
row 7 : marathon | 2:03:59 | haile gebrselassie | ethiopia | berlin, germany | september 28
*/

Question: 
in 2008 in track and field events who broke more world records, usain bolt or haile gebrselassie?

Reasoning Steps:
Step 1: Select relevant rows.
The question is aimed at determining which athlete, Usain Bolt or Haile Gebrselassie, broke more world records in 2008 in track and field events. We need to examine the performances of both athletes in the year 2008 to count the number of world records broken by each. The relevant rows are those where the athlete is either Usain Bolt or Haile Gebrselassie and the date is within the year 2008.
So we use f_select_row(row 1, row 2, row 3, row 7).

Step 2: Filter out useless columns.
similar words of the question link to columns:
in 2008 -> date
track and field events -> event
broke more world records -> athlete
usain bolt -> athlete
haile gebrselassie -> athlete
column value of the question link to columns:
2008 -> date
usain bolt -> athlete
haile gebrselassie -> athlete
semantic sentence of the question link to columns:
who broke more world records -> athlete
So we use f_select_column(event, athlete, date).

Step 3: The question is asking to compare the number of world records broken by Usain Bolt and Haile Gebrselassie in 2008. However, the provided data does not include a direct indicator of world records being broken; it only lists the events, athletes, and dates. To infer which athlete might have broken more records, we would need to focus on the events and the athlete's participation. Since both athletes are listed with multiple events, we can assume that each event could potentially represent a world record. We can use the f_group_column(athlete) operation to group the events by athlete to see how many events each athlete participated in, which might correlate with the number of world records broken.
So we use f_group_column(athlete).

Step 4: After using f_select_row(row 2, row 3, row 4, row 7), f_select_column(event, athlete, date) and f_group_column(athlete), we obtain the sub-table:
/*
col   : event           | athlete             | date
row 1 : 100 m           | usain bolt          | may 31
row 2 : 100 m           | usain bolt          | august 16
row 2 : 200 m           | usain bolt          | august 20
row 4 : marathon        | haile gebrselassie  | september 28
*/
/*
Group the rows according to column: athlete.
Group ID | athlete | Count
Group 1 | usain bolt | 3
Group 2 | haile gebrselassie | 1
*/
Based on the provided information, Usain Bolt participated in two events (100 m and 200 m) and Haile Gebrselassie participated in one event (marathon). However, the table does not specify which athletes broke world records. Since Usain Bolt has historically broken more world records in track and field, especially in the 100 m and 200 m events, and given his participation in two events compared to Haile Gebrselassie's one, it is reasonable to infer that Usain Bolt likely broke more world records in 2008.

Prediction Answer: 
usain bolt

Analysis:
Step 1 correctly identifies the relevant rows based on the criteria of the question (athletes being either Usain Bolt or Haile Gebrselassie and the date being within the year 2008). The selected rows (rows 2, 3, 4, and 7) are those where these conditions are met. Step 1 is correct.
Step 2 appropriately filters the columns to focus on the relevant information (event, athlete, and date) needed to answer the question. This step effectively narrows down the data to what is relevant for the comparison. Step 2 is correct.
Step 3 is unnecessary to create the sub-table by grouping the results and then counting them, but it doesn't affect the final answer. Step 3 is correct.
Step 4 correctly identifies that Usain Bolt broke more world records. Step 4 is correct.

Conclusion: [Correct]"""]

correct_5 = ["""Original Table:
/*
col : year | award | category | film | result
row 1 : 2009 | anandalok awards | anandalok awards for best actor | challenge | won
row 2 : 2009 | anandalok awards | anandalok awards for best action hero | challenge | won
row 3 : 2010 | star jalsha entertainment awards 2010 | star jalsha entertainment awards 2010 for best actor | poran jaye jolia re | won
row 4 : 2010 | star jalsha entertainment awards 2010 | star jalsha entertainment awards 2010 for best actor | dujone | nominated
row 5 : 2010 | tele cine awards 2010 | tele cine awards 2010 for best actor | challenge | won
row 6 : 2010 | kalakar awards 2010 | kalakar awards 2010 for best actor | challenge | won
row 7 : 2010 | star ananda shera bangali awards 2010 | star ananda shera notun protibha award |  | won
row 8 : 2010 | anandalok awards 2010 | anandalok awards 2010 for best actor (male) | le chakka | won
row 9 : 2011 | big bangla movie awards 2011 | big bangla movie awards 2011 for best actor of the decade |  | won
row 10 : 2011 | anandalok awards | anandalok awards for best actor | paglu | nominated
*/

Question: 
how many times, total, was the result "won"

Reasoning Steps:
Step 1: Filter out useless columns.
similar words of the question link to columns:
times -> result
the result "won" -> result
semantic sentence of the question link to columns:
None
So we use f_select_column(result).

Step 2: The question aims to find the total number of times the result was "won". Since the "result" column contains the outcomes for each entry, we can use the f_group_column(result) operation to group the results and count the occurrences of "won".
So we use f_group_column(result).

Step 3: After using f_select_column(result) and f_group_column(result), we obtain the sub-table:
/*
col : result
row 1 : won
row 2 : won
row 3 : won
row 4 : nominated
row 5 : won
row 6 : won
row 7 : won
row 8 : won
row 9 : won
row 10 : nominated
*/
/*
Group the rows according to column: result.
Group ID | result | Count
Group 1 | won | 8
Group 2 | nominated | 2
*/
The result "won" appears 8 times in the table.

Prediction Answer: 
8

Analysis:
Step 1 correctly filters the columns to focus only on the "result" column, which is directly relevant to the question of counting how many times the result was "won". This step ensures that only the necessary data is retained for the next steps. Step 1 is correct.
Step 2 is unnecessary to create the sub-table by grouping the results and then counting them, but it doesn't affect the final answer. Step 2 is correct.
Step 3 correctly indicates the total time of result "won". Step 3 is correct.

Conclusion: [Correct]"""]

wrong_1 = ["""Original Table:
/*
col   : goal | date         | location          | opponent | lineup              | min | assist/pass | score | result | competition
row 1 : 1    | may 9, 2004  | usaalbuquerque nm | mexico   | on 70' (off lilly)  | 19  | tarpley     | 3–0   | 3–0    | friendly
row 2 : 2    | jun 26, 2005 | usavirginia beach | canada   | 90.start            | 12  | unassisted  | 1–0   | 2–0    | friendly
row 3 : 3    | jan 30, 2007 | chnguangzhou      | china pr | 90.start            | 46+ | unassisted  | 1–0   | 2–0    | four nations tournament
row 4 : 4    | may 12, 2007 | usafrisco tx      | canada   | off 72' (on wagner) | 28  | tarpley     | 3–1   | 6–2    | friendly
row 5 : 5    | sep 18, 2007 | chnshanghai       | nigeria  | 90.start            | 1   | wambach     | 1–0   | 1–0    | world cup – group b
row 6 : 6    | sep 30, 2007 | chnshanghai       | norway   | 90.start            | 58  | unassisted  | 3–0   | 4–1    | world cup final - third place playoff
row 7 : 7    | aug 18, 2008 | chnbeijing        | japan    | 90.start            | 44  | rodriguez   | 2–1   | 4–2    | olympics tournament
row 8 : 8    | sep 20, 2008 | usabridgeview il  | ireland  | 90.start            | 19  | tarpley     | 1–0   | 2–0    | friendly
*/

Question:
how many consecutive friendly competitions did chalupny score in?

Reasoning Steps:
Step 1: Select relevant rows.
The question aims to find out the number of consecutive friendly competitions in which Chalupny scored. We need to look at the rows where the competition type is "friendly" and check the dates to determine if they are consecutive. The relevant rows are row 1, row 2, and row 4. So we use f_select_row(row 1, row 2, row 4).

Step 2: Filter out useless columns.
similar words of the question link to columns :
scored in -> goal
consecutive -> date
friendly competitions -> competition
column value link to columns :
friendly -> competition
So we use f_select_column(goal, date, competition).
  
Step 3: Group the column of competition. So we use f_group_column(competition).

Step 4: After using f_select_row(row 1, row 2, row 4), f_select_column(goal, date, competition) and f_group_column(competition), we obtain the sub table:
/*
col : goal |       date  | competition
row 1 : 1 | may 9, 2004 | friendly
row 2 : 2 | jun 26, 2005 | friendly
row 3 : 4 | may 12, 2007 | friendly
*/
/*
Group the rows according to column: competition.
Group ID | competition | Count
Group 1 | friendly | 3
*/
Chalupny did not score in any consecutive friendly competitions. The gaps in dates between her goals indicate non-consecutive friendly matches.

Prediction Answer:
0

Analysis:
Row 8 was omitted in Step 1, despite satisfying the criteria. The reasoning only considers rows 1, 2, and 4, which makes Step 1 incomplete and therefore incorrect. Step 1 is incorrect.

Conclusion: (sub-table error -> row error -> <END>)"""]

wrong_2 = ["""Original Table:
/*
col   : seasons | team                                  | ch.wins | promotions | relegations
row 1 : 5       | pistoia basket 2000                   | 0       | 0          | 0
row 2 : 4       | juve caserta basket                   | 0       | 1          | 0
row 3 : 3       | gruppo triboldi basket soresina       | 0       | 1          | 0
row 4 : 3       | nuova sebastiani rieti                | 1       | 1          | 0
row 5 : 3       | progresso castelmaggiore              | 0       | 0          | 0
row 6 : 3       | orlandina basket                      | 1       | 1          | 1
row 7 : 3       | sutor basket montegranaro             | 0       | 1          | 1
row 8 : 3       | virtus ragusa                         | 0       | 0          | 1
row 9 : 3       | robur basket osimo                    | 0       | 0          | 1
row 10 : 3       | reyer venezia                         | 0       | 1          | 0
row 11 : 3       | new basket brindisi                   | 1       | 2          | 0
*/

Question:
who had the most promotions, nuova sebastiani rieti or new basket brindisi?

Reasoning Steps:
Step 1: Select relevant rows.
The question aims to compare the number of promotions between Nuova Sebastiani Rieti and New Basket Brindisi. We need to locate the rows for these two teams and compare their "promotions" column values to determine which team had more promotions. So we use f_select_row(row 4, row 6)

Step 2: Filter out useless columns.
similar words of the question link to columns:
had the most promotions -> promotions
between the two teams -> team
column value of the question link to columns:
nuova sebastiani rieti -> team
new basket brindisi -> team
semantic sentence of the question link to columns:
who had the most promotions -> promotions
So we use f_select_column(team, promotions).

Step 3: After using f_select_row(row 4, row 6) and f_select_column(team, promotions), we obtain the sub-table:
/*
col   : team                   | promotions
row 1 : nuova sebastiani rieti | 1
row 2 : orlandina basket       | 1
*/
The table does not include a row for "new basket brindisi". However, both "nuova sebastiani rieti" and "orlandina basket" have 1 promotion each. Since there is no comparison available for "new basket brindisi", we cannot determine if it has more promotions than "nuova sebastiani rieti". Based on the provided data, both teams mentioned have the same number of promotions.

Prediction Answer: 
Both "nuova sebastiani rieti" and "orlandina basket" have 1 promotion. There is no information about "new basket brindisi" in the table.

Analysis: 
Step 1 correctly identifies the relevant row for the team Nuova Sebastiani Rieti. However, there is an issue because the row for New Basket Brindisi (row 11) is not included in the selected rows. Step 1 is incorrect.

Conclusion: (sub-table error -> row error -> <END>)"""]

wrong_3 = ["""Original Table:
/*
col   : club                                | founded | nickname  | location           | home ground                  | entered competition | most recent promotion
row 1 : bundoora football club              | 1974    | bulls     | bundoora           | yulong reserve               | 1981                | 1982
row 2 : eltham football club                | 1909    | panthers  | eltham             | central park                 | 1922                | 2003
row 3 : greensborough football club         | 1905    | boro      | greensborough      | war memorial park            | 1922                | 2007
row 4 : heidelberg football club            | 1876    | tigers    | heidelberg         | warringal park               | 1923                | 1983
row 5 : lalor football club                 | 1955    | bloods    | lalor              | lalor reserve                | 1968                | 2011
row 6 : macleod football club               | 1946    | kangaroos | rosanna            | de winton park               | 1947                | 2010
row 7 : montmorency football club           | 1924    | magpies   | montmorency        | montmorency park, north oval | 1924                | n/a
row 8 : north heidelberg football club      | 1958    | bulldogs  | heidelberg heights | shelley street reserve       | 1958                | n/a
row 9 : northcote park football club        | 1952    | cougars   | northcote          | bill lawry oval              | 1982                | 1995
row 10 : west preston lakeside football club | 1998    | roosters  | reservoir          | j e moore park               | 1996                | 1997
*/

Question:
how many division 1 teams were founded before 1950?

Reasoning Steps:
Step 1: Select relevant rows. 
The question aims to find out the number of Division 1 teams that were founded before the year 1950. We need to look at the "founded" column and count the number of teams that meet this criterion. So we use f_select_row(row 2, row 3, row 4, row 8).

Step 2: Filter out useless columns.
similar words of the question link to columns :
division 1 teams -> club
founded before 1950 -> found
column value of the question link to columns :
1950 -> found
semantic sentence of the question link to columns :
None
So we use f_select_column(club, found).

Step 3: After using f_select_row(row 2, row 3, row 4, row 8) and f_select_column(club, found), we obtain the sub table:
/*
col   : club                            | founded
row 1 : eltham football club            | 1909
row 2 : greensborough football club     | 1905
row 3 : heidelberg football club        | 1876
row 4 : north heidelberg football club  | 1958
*/
The clubs founded before 1950 that are in Division 1 are Eltham Football Club, Greensborough Football Club, and Heidelberg Football Club.

Prediction Answer:
3

Analysis:
Step 1 is incorrect as it misses some of the relevant rows. While it correctly includes row 2, row 3, and row 4, it wrongly includes row 8 which was founded in 1958 and thus doesn't meet the "founded before 1950" criterion. Additionally, it fails to include other rows like row 6 (founded in 1946) and row 7 (founded in 1924) as it meets the condition of being founded before 1950. This step is flawed in its selection of rows and thus incorrect. Step 1 is incorrect.

Conclusion: (sub-table error -> row error -> <END>)"""]

wrong_4 = ["""Original Table:
/*
col   : finished | horse         | jockey       | trainer      | owner               | time / behind
row 1 : 1st      | spokane       | tom kiley    | john rodegap | noah armstrong      | 2:34.50
row 2 : 2nd      | proctor knott | s. barnes    |              | scoggan & bryant    | nose
row 3 : 3rd      | once again    | isaac murphy |              | milton young        | 2
row 4 : 4th      | hindoocraft   | armstrong    |              | scoggan bros.       | 1
row 5 : 5th      | cassius       | f. taral     |              | beverwyck stable    | 1
row 6 : 6th      | sportsman     | i. lewis     |              | j.k. megibben & co. | 1/2
row 7 : 7th      | outbound      | hollis       |              | fleetwood stable
row 8 : 8th      | bootmaker     | warwick      |              | wilson & young
*/

Question:
who came in first?

Reasoning Steps:
Step 1: Select relevant rows. 
The question aims to find out which horse and its corresponding details came in first place. We need to look at the "finished" column to identify the row where the value is "1st".
So we use f_select_row(row 1).

Step 2: Filter out useless columns.
similar words of the question link to columns:
came in first -> finished
column value of the question link to columns:
1st -> finished
semantic sentence of the question link to columns:
None
So we use f_select_column(finished).

Step 3: After using f_select_row(row 1) and f_select_column(finished), we obtain the sub table:
/*
col   : finished
row 1 : 1st
*/
The information provided only states that someone or something came in 1st, but it does not specify who or what entity achieved that position.


Prediction Answer:
Not specified in the given data.

Analysis:
Step 1 correctly identifies the relevant row which corresponds to the first place finisher. By looking at the 'finished' column and selecting the row where the value is '1st', it picks out the appropriate data point for further analysis. Step 1 is correct.
Step 2 incorrectly filters out almost all the useful columns. The question asks for the entity that came in first, which means we need to retain the 'horse', 'jockey', 'trainer', and 'owner' columns to provide a complete answer. Filtering out these columns leaves insufficient information to identify who came in first. Step 2 is incorrect.

Conclusion: (sub-table error -> column error -> <END>)"""]

wrong_5 = ["""Original Table:
/*
col   : res. | record | opponent         | method                        | event                                        | date               | round | time | location                                | notes
row 1 : win  | 12-3   | mike hayes       | ko (punch)                    | ksw 25: khalidov vs. sakurai                 | december 7, 2013   | 1     | 1:12 | wrocław, poland
row 2 : win  | 11–3   | nick moghadden   | tko (punches)                 | bellator 99                                  | september 13, 2013 | 1     | 3:22 | temecula, california, united states     | bellator debut
row 3 : loss | 10–3   | guto inocente    | decision (unanimous)          | strikeforce: barnett vs. cormier             | may 19, 2012       | 3     | 5:00 | san jose, california, united states     | light heavyweight debut
row 4 : win  | 10–2   | brett albee      | tko (strikes)                 | strikeforce: diaz vs. daley                  | april 9, 2011      | 1     | 1:46 | san diego, california, united states
row 5 : loss | 9–2    | lavar johnson    | ko (punches)                  | strikeforce challengers: bowling vs. voelker | october 22, 2010   | 1     | 2:17 | fresno, california, united states
row 6 : win  | 9–1    | eddie sapp       | submission (rear-naked choke) | native fighting championship 6               | august 14, 2010    | 1     | 2:01 | campo, california, united states
row 7 : loss | 8–1    | cody goodale     | decision (unanimous)          | gladiator challenge: maximum force           | april 25, 2010     | 3     | 5:00 | san jacinto, california, united states
*/

Question:
how many loses did virgil zwicker have?

Reasoning Steps:
Step 1: Select relevant rows.
The question aims to find out the number of losses Virgil Zwicker had based on the provided fight records. We need to count the rows where the "res." column shows "loss".
So we use f_select_row(row 3, row 5, row 7).

Step 2: Filter out useless columns.
similar words of the question link to columns:
loses -> record
column value of the question link to columns:
10–3 -> record
semantic sentence of the question link to columns:
None
So we use f_select_column(record).

Step 3: After using f_select_row(row 3, row 5, row 7) and f_select_column(record), we obtain the sub table:
/*
col   : record
row 1 : 10–3
row 2 : 9–2
row 3 : 8–1
*/
The provided table shows records of wins and losses but does not specify who the records belong to. However, if we assume that the table represents Virgil Zwicker's records, then we can deduce the number of losses from each record. The losses in the records are 3, 2, and 1 respectively. If we consider each row as a separate season or period, then the total number of losses would be the sum of these losses: 3 + 2 + 1 = 6.

Prediction Answer:
6

Analysis:
Step 1 correctly identifies the relevant rows where the "res." column indicates a loss. The rows selected are indeed the ones where the outcome is a loss. Step 1 is correct.
Step 2 incorrectly filters out the columns. The question asks for the number of losses, but the filtering step selects only the 'record' column, which combines wins and losses in a single string (e.g., "10–3"). This does not directly provide the number of losses. Instead, the 'res.' column should be used to count the losses directly. Step 2 is incorrect.

Conclusion: (sub-table error -> column error -> <END>)"""]

wrong_6 = ["""Original Table:
/*
col   : date             | home team         | score | away team       | notes
row 1 : 17 december 2007 | foolad            | 4-4   | esteghlal ahvaz | foolad progress 8-7 on penalties
row 2 : 21 december 2007 | rah ahan          | 2-2   | steel azin      | rah ahan progress 5-2 on penalties
row 3 : 21 december 2007 | zob ahan          | 1-1   | esteghlal       | esteghlal progress 3-1 on penalties
row 4 : 21 december 2007 | bargh shiraz      | 1-0   | paykan tehran
row 5 : 21 december 2007 | shahin bushehr    | 2-2   | saba battery    | shahin bushehr progress 6-5 on penalties
row 6 : 24 december 2007 | pas hamedan       | 3-0   | persepolis
row 7 : 26 february 2008 | moghavemat sepasi | 1-2   | sepahan
row 8 : 4 march 2008     | sanaye arak       | 0-1   | pegah gilan
*/


Question:
what is the average score of all home team members for all dates?

Reasoning Steps:
Step 1: Add necessary columns to the table.
The question asks about the average score of all home team members for all dates. We need to know the score of each match, which is given in the "score" column. The scores are in the format home-team-score-away-team-score. We extract the home team score for each row and create a different column "home team score" for each row. The datatype is numerical. So we use f_add_column(home team score). The value: 4 | 2 | 1 | 1 | 2 | 3 | 1 | 0

Step 2: Filter out useless columns.
similar words of the question link to columns :
score -> home team score
column value of the question link to columns :
None
semantic sentence of the question link to columns :
None
So we use f_select_column(home team score).

Step 3: After using f_add_column(home team score) and f_select_column(home team score), we obtain the sub table:
/*
col   :  home team score
row 1 :  4
row 2 :  2
row 3 :  1
row 4 :  1
row 5 :  2
row 6 :  3
row 7 :  1
row 8 :  0
*/
The average score of all home team members for all dates can be calculated by adding all the scores together and dividing by the number of rows. The sum of all scores is 17 (4+2+1+1+2+3+1+0) and there are 8 rows. Therefore, the average score is 2.125.

Prediction Answer:
2.125

Analysis:
Step 1 makes a correct attempt at extracting the home team score from the given "score" column. By creating a new column and populating it with the appropriate values based on the format of the scores provided in the original table, it sets up the data in a way that can be used for further calculation related to the home team scores. Step 1 is correct.
Step 2 effectively filters the columns to focus only on the newly created "home team score" column, which is the relevant data needed to calculate the average score of the home team members as asked in the question. This step is a proper way to narrow down the data for the subsequent calculation step. Step 2 is correct.
Step 3 has a calculation error. When adding up the scores (4 + 2 + 1 + 1 + 2 + 3 + 1 + 0), the sum is indeed 14, not 17 as stated. Step 3 is incorrect.

Conclusion: (final query error -> <END>)"""]

if __name__=="__main__":
    data_dict = {
        "incorrect_6":wrong_6,
        "incorrect_1":wrong_1,
        "incorrect_2":wrong_2,
        "incorrect_3":wrong_3,
        "incorrect_4":wrong_4,
        "incorrect_5":wrong_5,
    }
    file_path = "critic/TableQA/tools/few_shot_tree.json"

    with open(file_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)