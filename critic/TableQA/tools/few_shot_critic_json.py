import json
row_error = [
    """Original Table:
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

Critique:
Row 8 was omitted in Step 1, despite satisfying the criteria. The reasoning only considers rows 1, 2, and 4, which makes Step 1 incomplete and therefore incorrect. Step 1 is incorrect.

Conclusion: [Incorrect] Step 1""",
"""Original Table:
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

Critique: 
Step 1 correctly identifies the relevant row for the team Nuova Sebastiani Rieti. However, there is an issue because the row for New Basket Brindisi (row 11) is not included in the selected rows. Step 1 is incorrect.

Conclusion: [Incorrect] Step 1""",
"""Original Table:
/*
col   : place | position | number | name             | league two | fa cup | league cup | fl trophy | total
row 1 : 1     | mf       | 4      | ryan hall        | 10         | 1      | 0          | 3         | 14
row 2 : 2     | df       | 6      | bilel mohsni     | 13         | 0      | 0          | 0         | 13
row 3 : 3     | fw       | 22     | liam dickinson   | 10         | 1      | 0          | 1         | 12
row 4 : 4     | fw       | 9      | neil harris      | 9          | 0      | 0          | 1         | 10
row 5 : =     | df       | 3      | peter gilbert    | 3          | 0      | 0          | 0         | 3
row 6 : 6    | fw       | 24     | elliot benyon    | 2          | 0      | 0          | 0         | 2
row 7 : =     | fw       | 37     | freddy eastwood  | 2          | 0      | 0          | 0         | 2
row 8 : 8    | mf       | 18     | ryan leonard     | 1          | 0      | 0          | 0         | 1
row 9 : =     | fw       | 21     | blair sturrock   | 0          | 0      | 0          | 1         | 1
*/

Question:
what player has one fa cup and one fl trophy?

Reasoning Steps:
Step 1: Select relevant rows.
The question is asking for a player who has scored exactly one goal in the FA Cup and one goal in the FL Trophy. We need to look for a row where the 'FA Cup' column shows 1 and the 'FL Trophy' column also shows 1.
So we use f_select_row(row 9).

Step 2: Filter out useless columns.
similar words of the question link to columns:
player -> name
one fa cup -> fa cup
one fl trophy -> fl trophy
column value of the question link to columns:
1 -> fa cup, fl trophy
semantic sentence of the question link to columns:
None
So we use f_select_column(name, fa cup, fl trophy).

Step 3: After using f_select_row(row 9) and f_select_column(name, fa cup, fl trophy), we obtain the sub table:
/*
col   : name           | fa cup | fl trophy
row 1 : blair sturrock | 0      | 1
*/
The player who has one FA Cup and one FL Trophy is Blair Sturrock. However, based on the provided data, Blair Sturrock has 0 FA Cups and 1 FL Trophy, not both one FA Cup and one FL Trophy. Therefore, there is no player in the given data who meets the criteria.

Prediction Answer:
None

Critique:
Step 1 correctly identifies row 9 as a potential candidate because the 'FL Trophy' column shows 1. However, this step overlooks the necessity to check both conditions simultaneously (having exactly 1 FA Cup and 1 FL Trophy). Step 1 is incorrect.

Conclusion: [Incorrect] Step 1""",
"""Original Table:
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

Critique:
Step 1 is incorrect as it misses some of the relevant rows. While it correctly includes row 2, row 3, and row 4, it wrongly includes row 8 which was founded in 1958 and thus doesn't meet the "founded before 1950" criterion. Additionally, it fails to include other rows like row 6 (founded in 1946) and row 7 (founded in 1924) as it meets the condition of being founded before 1950. This step is flawed in its selection of rows and thus incorrect. Step 1 is incorrect.

Conclusion: [Incorrect] Step 1""",
"""Original Table:
/*
col   : club                     | league              | sport             | venue                               | established | championships
row 1 : madison mustangs         | ifl                 | american football | breitenbach stadium                 | 1997        | 4 consecutive ironbowls
row 2 : madison mallards         | nl                  | baseball          | warner park                         | 2001        | 1 championship
row 3 : madison 56ers            | npsl                | soccer            | breese stevens field                | 2005        | 0 championships
row 4 : wisconsin rugby club     | wrfu                | rugby             | wisconsin rugby club sports complex | 1962        | 2 championships
row 5 : madison minotaurs        | wrfu                | rugby             | yahara rugby field                  | 2007        | 0 bingham cups
row 6 : wisconsin badgers        | big ten, ncaa div.1 | 23 varsity teams  | camp randall stadium, kohl center   | 1849        | 27 championships
row 7 : edgewood eagles          | nacc, ncaa div.3    | 16 varsity teams  | edgedome                            | 1974        | 35 championships
row 8 : madison college wolfpack | n4c, njcaa div.3    | 8 varsity teams   | redsten gymnasium, roberts field    | 1912        | 21 championships
row 9 : mad rollin' dolls        | wftda               | roller derby      | alliant energy center               | 2005        | 0 championships
row 10 : madison blues            | glhl                | hockey            | capitol ice arena                   | 2010        | 0 championships
*/

Question:
how many current teams have been in existence for 25 years or greater?

Reasoning Steps:
Step 1: Select relevant rows.
The question aims to identify the number of teams that have existed for 25 years or more. We need to look at the "established" column and filter the rows based on the year being 1998 or earlier.
So we use f_select_row(row 1, row 4, row 6, row 8).

Step 2: Filter out useless columns.
similar words of the question link to columns:
how many current teams -> club
have been in existence -> established
for 25 years or greater -> established
column value of the question link to columns:
25 years or greater -> established
semantic sentence of the question link to columns:
None
So we use f_select_column(club, established).

Step 3: After using f_select_row(row 1, row 4, row 6, row 8) and f_select_column(club, established), we obtain the sub table:
/*
col   : club                     | established
row 1 : madison mustangs         | 1997
row 2 : wisconsin rugby club     | 1962
row 3 : wisconsin badgers        | 1849
row 4 : madison college wolfpack | 1912
*/
The Wisconsin Rugby Club was established in 1962, the Wisconsin Badgers in 1849, and the Madison College Wolfpack in 1912. All of these clubs have been in existence for more than 25 years. The Madison Mustangs were established in 1997, which is less than 25 years from the current year (assuming the current year is 2023). Therefore, the number of current teams that have been in existence for 25 years or greater is 3.

Prediction Answer:
3

Critique:
Step 1 partially identifies the relevant rows that have existed for 25 years or more. The selected rows (row 4, row 6, row 8) are based on the "established" year being 1998 or earlier. However, this step incorrectly includes row 1 as relevant and misses row 7 (Edgewood Eagles, established in 1974), which also meets the criteria. This misjudgment and omission render Step 1 incomplete and incorrect.

Conclusion: [Incorrect] Step 1"""
]

column_error = [
    """Original Table:
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

Critique:
Step 1 correctly identifies the relevant row which corresponds to the first place finisher. By looking at the 'finished' column and selecting the row where the value is '1st', it picks out the appropriate data point for further analysis. Step 1 is correct.
Step 2 incorrectly filters out almost all the useful columns. The question asks for the entity that came in first, which means we need to retain the 'horse', 'jockey', 'trainer', and 'owner' columns to provide a complete answer. Filtering out these columns leaves insufficient information to identify who came in first. Step 2 is incorrect.

Conclusion: [Incorrect] Step 2""",
"""Original Table:
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

Critique:
Step 1 correctly identifies the relevant rows where the "res." column indicates a loss. The rows selected are indeed the ones where the outcome is a loss. Step 1 is correct.
Step 2 incorrectly filters out the columns. The question asks for the number of losses, but the filtering step selects only the 'record' column, which combines wins and losses in a single string (e.g., "10–3"). This does not directly provide the number of losses. Instead, the 'res.' column should be used to count the losses directly. Step 2 is incorrect.

Conclusion: [Incorrect] Step 2""",
"""Original Table:
/*
col   : year | song                                               | chart positions\nus country | chart positions\ncan country | album
row 1 : 1968 | "god help you woman"                               | 32                          | 24                           | singles only
row 2 : 1969 | "please take me back"                              | 40                          | —                            | singles only
row 3 : 1969 | "i'm not through loving you"                       | 52                          | —                            | singles only
row 4 : 1969 | "molly"                                            | 53                          | —                            | singles only
row 5 : 1984 | "if i could only dance with you"                   | 10                          | 10                           | the man in the mirror
row 6 : 1984 | "you're gettin' to me again"                       | 1                           | 3                            | the man in the mirror
row 7 : 1984 | "let me down easy"                                 | 16                          | 33                           | the man in the mirror
row 8 : 1985 | "i'll be your fool tonight"                        | 54                          | —                            | past the point of no return
*/

Question:
which track is at the top of the us chart?

Reasoning Steps:
Step 1: Filter out useless columns.
similar words of the question link to columns:
track -> song
at the top of the us chart -> chart positions\\nus country
column value of the question link to columns:
1 -> chart positions\\nus country
semantic sentence of the question link to columns:
which track is at the top of the us chart -> song, chart positions\\nus country
So we use f_select_column(song, album).

Step 2: After using f_select_column(song, album), we obtain the sub table:
/*
row 1 : "god help you woman"                               | singles only
row 2 : "please take me back"                              | singles only
row 3 : "i'm not through loving you"                       | singles only
row 4 : "molly"                                            | singles only
row 5 : "if i could only dance with you"                   | the man in the mirror
row 6 : "you're gettin' to me again"                       | the man in the mirror
row 7 : "let me down easy"                                 | the man in the mirror
row 8 : "i'll be your fool tonight"                        | past the point of no return
*/
The question asks for the track at the top of the US chart, but the provided data does not include any information about chart positions or rankings. Therefore, based on the given data, it is impossible to determine which track is at the top of the US chart.

Prediction Answer:
Cannot determine from the given data.

Critique:
Step 1 incorrectly filters out the columns. The question asks for the track that is at the top of the US chart, which requires both the "song" and "chart positions\nus country" columns to identify the song with the highest position. The step omits the crucial "chart positions\nus country" column, making it impossible to determine the answer. Step 1 is incorrect.

Conclusion: [Incorrect] Step 1"""
]

query_error = [
    """Original Table:
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

Critique:
Step 1 makes a correct attempt at extracting the home team score from the given "score" column. By creating a new column and populating it with the appropriate values based on the format of the scores provided in the original table, it sets up the data in a way that can be used for further calculation related to the home team scores. Step 1 is correct.
Step 2 effectively filters the columns to focus only on the newly created "home team score" column, which is the relevant data needed to calculate the average score of the home team members as asked in the question. This step is a proper way to narrow down the data for the subsequent calculation step. Step 2 is correct.
Step 3 has a calculation error. When adding up the scores (4 + 2 + 1 + 1 + 2 + 3 + 1 + 0), the sum is indeed 14, not 17 as stated. Step 3 is incorrect.

Conclusion: [Incorrect] Step 3""",
"""Original Table:
/*
col   : week | date    | opponent                     | score | result | record
row 1 : 1    | july 9  | vs. saskatchewan roughriders | 31–21 | win    | 1–0
row 2 : 2    | july 24 | vs. hamilton tiger-cats      | 36–25 | loss   | 2–1
row 3 : 3    | aug 1   | at edmonton eskimos          | 32–26 | win    | 3–1
row 4 : 4    | aug 8   | vs. bc lions                 | 29–16 | win    | 4–1
row 5 : 5    | aug 20  | at calgary stampeders        | 35–4  | win    | 5–1
row 6 : 6    | sept 11 | vs. calgary stampeders       | 15–11 | loss   | 7–2
row 7 : 7   | sept 18 | at ottawa rough riders       | 38–28 | loss   | 7–3
row 8 : 8   | sept 25 | vs. montreal concordes       | 19–16 | win    | 8–3
row 9 : 9   | oct 2   | at bc lions                  | 29–19 | win    | 9–3
row 10 : 10   | oct 23  | vs. edmonton eskimos         | 33–17 | loss   | 11–4
row 11 : 11   | nov 7   | at hamilton tiger-cats       | 24–21 | loss   | 11–5
*/

Question:
what is the average number of points scored by opponents in the five games lost this season?

Reasoning Steps:
Step 1: Select relevant rows. 
The question aims to calculate the average number of points scored by opponents in the games that were lost during the season. We need to identify the rows representing the games that ended in a loss, note the scores of the opponents in those games, and then calculate the average of those scores. So we use f_select_row(row 2, row 6, row 7, row 10, row 11).

Step 2: Filter out useless columns.
similar words of the question link to columns :
the average number of points scored -> score
by opponents -> opponent
in the five games lost -> result
column value of the question link to columns :
loss -> result
semantic sentence of the question link to columns :
what is the average number of points scored by opponents in the five games lost -> opponent, score
So we use f_select_column(opponent, score, result).

Step 3: After using f_select_row(row 2, row 6, row 7, row 10, row 11) and f_select_column(opponent, score, result), we obtain the sub table:
/*
col   : opponent                | score | result
row 1 : vs. hamilton tiger-cats | 36–25 | loss
row 2 : vs. calgary stampeders  | 15–11 | loss
row 3 : at ottawa rough riders  | 38–28 | loss
row 4 : vs. edmonton eskimos    | 33–17 | loss
row 5 : at hamilton tiger-cats  | 24–21 | loss
*/
The scores for the opponents in the five lost games are as follows:
Hamilton Tiger-Cats: 36
Calgary Stampeders: 15
Ottawa Rough Riders: 38
Edmonton Eskimos: 33
Hamilton Tiger-Cats: 24
By adding these scores together and dividing by 5, we get the average number of points scored by opponents in the five games lost this season, which is 30.

Prediction Answer:
30

Critique:
Step 1 correctly identifies the relevant rows which correspond to the games that were lost during the season. By looking at the 'result' column and selecting the rows where the result is 'loss', it picks out the appropriate data points for further analysis. Step 1 is correct.
Step 2 filters the necessary columns (opponent, score, and result) to focus only on the information relevant to answering the question. This step is a valid approach as it narrows down the data to what is needed to calculate the average points scored by opponents in the lost games. Step 2 is correct.
Step 3 correctly extracts the opponents' scores as 36 (from 36–25), 15 (from 15–11), 38 (from 38–28), 33 (from 33–17), and 24 (from 24–21). But there was a miscalculation either in adding the scores together or in the division to find the average. Step 3 is incorrect.

Conclusion: [Incorrect] Step 3""",
"""Original Table:
/*
col   : tie | home team              | score | away team          | attendance
row 1 : 1   | aylesbury united       | 2-2   | windsor & eton     | 847
row 2 : 2   | burscough              | 5-0   | wakefield & emley  | 437
row 3 : 3   | dover athletic         | 0-3   | forest green roves | 932
row 4 : 4   | farnborough town       | 2-0   | halifax town       | 863
row 5 : 5   | gloucester city        | 1-1   | southport          | 1,237
row 6 : 6   | havant & waterlooville | 3-0   | hayes              | 456
row 7 : 7   | margate                | 0-2   | tamworth           | 971
row 8 : 8   | yeovil town            | 2-1   | northwich victoria | 4,469
*/

Question:
how many games attendance was under 1000?

Reasoning Steps:
Step 1: Select relevant rows. 
The question aims to find out how many games had an attendance of less than 1000 people. To answer this, we need to count the number of rows where the attendance column shows a number less than 1000. So we use f_select_row(row 1, row 2, row 3, row 4, row 6, row 7).

Step 2: Filter out useless columns.
similar words of the question link to columns :
under 1000 -> attendance
column value of the question link to columns :
1000 -> attendance
semantic sentence of the question link to columns :
None
So we use f_select_column(attendance).

Step 3: After using f_select_row(row 1, row 2, row 3, row 4, row 6, row 7) and f_select_column(attendance), we obtain the sub table:
/*
col   : attendance
row 1 : 847
row 2 : 437
row 3 : 932
row 4 : 863
row 5 : 456
row 6 : 971
*/
The games with attendance under 1000 were rows 1, 2, 4, and 5. Therefore, there were 4 games with attendance under 1000.

Prediction Answer:
4

Critique:
Step 1 correctly selects the rows that are relevant for further analysis regarding the attendance being under 1000. It includes all the rows where the attendance values might potentially be less than 1000, which are row 1, row 2, row 3, row 4, row 6, and row 7. This step makes the proper initial identification based on the condition stated in the question. Step 1 is correct.
Step 2 filters out the columns effectively by choosing the "attendance" column. Since the question is focused on the attendance values to determine which are under 1000, this step narrows down the data to just what's needed for the subsequent steps. Step 2 is correct.
Step 3 makes an error in counting the number of games with attendance under 1000. Looking at the sub-table from Step 3, all the rows shown (row 1 with 847, row 2 with 437, row 3 with 932, row 4 with 863, row 5 with 456, row 6 with 971) have attendance values that are less than 1000. Step 3 is incorrect.

Conclusion: [Incorrect] Step 3"""
]

def critic_tree_init(file_path = "critic/TableQA/tools/few_shot_critic.json"):

    data_dict = {
        "sub-table error":[
            row_error[0]
        ],
        "final query error":[query_error[0]]

    }

    with open(file_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)


if __name__=="__main__":

    critic_tree_init()