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

Statement:
he bombers scored a total of 58 points against the BC Lions.

Prediction Answer:
YES

Explanation: The question asks how many total points the Bombers scored against the BC Lions. From the original table, the relevant rows are:
Row 5: On Aug 8, the Bombers played against the BC Lions and scored 29 points.
Row 9: On Oct 2, the Bombers played against the BC Lions again and scored 29 points.
Therefore, the total points scored by the Bombers against the BC Lions is: 29 + 29 = 58 points.
So the Prediction Answer YES is correct.

Conclusion: [Correct]"""]

correct_2 = ["""Original Table:
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

Statement: 
haile gebrselassie broke more world records in 2008 in track and field events

Prediction Answer: 
NO

Explanation: Based on the original table, we can determine the world records set by Usain Bolt and Haile Gebrselassie in 2008:
Usain Bolt:
In the 100m event, Usain Bolt ran a time of 9.72 seconds (May 31, New York City, USA), which was a world record.
In another 100m event, Usain Bolt ran a time of 9.69 seconds (august 16, Beijing, China), which was a world record.
In the 200m event, Usain Bolt ran a time of 19.30 seconds (August 20, Beijing, China), which was also a world record.
In the 4x100m relay, the Jamaican team ran a time of 37.10 seconds (August 22, Beijing, China), which was another world record.
Haile Gebrselassie:
In the marathon event, Haile Gebrselassie completed the race in 2:03:59 (September 28, Berlin, Germany), which was a world record.
From the table, it is clear that Usain Bolt set three world records in 2008 (100m, 100m, 200m, and 4x100m relay), whereas Haile Gebrselassie set only one world record in 2008.
So the Prediction Answer NO is correct.
             
Conclusion: [Correct]"""]

correct_3 = ["""Original Table:
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

Statement:
the election of 2007 was the first to reach over 40% of the popular vote

Prediction Answer:
NO

Explanation: Based on the original table, the question asks for the first election where the percentage of popular votes exceeded 40%.
The table shows the percentage of popular votes for each election:
1988: 22.16%
1991: 32.11%
1994: 35.34%
1999: 33.45%
2003: 44.67%
2007: 39.15%
2011: 39.34%
The first election to reach over 40% is the 2003 election with 44.67% of the popular vote.
Therefore, the Prediction Answer of NO is correct.

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

Statement:
chalupny scored in 0 consecutive friendly competitions

Prediction Answer:
YES

Explanation: 
We can see that Chalupny scored in the following consecutive friendly competitions:
On May 9, 2004, against Mexico.
On Jun 26, 2005, against Canada
These two instances represent consecutive friendly competitions in which Chalupny scored. Therefore, the Prediction Answer of YES is incorrect.

Conclusion: [Incorrect]"""]

wrong_2 = ["""Original Table:
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

Statement:
there are 5 division 1 teams that were founded before 1950

Prediction Answer:
NO

Explanation: Bundoora Football Club – Founded in 1974 (not before 1950)
Eltham Football Club – Founded in 1909 (before 1950)
Greensborough Football Club – Founded in 1905 (before 1950)
Heidelberg Football Club – Founded in 1876 (before 1950)
Lalor Football Club – Founded in 1955 (not before 1950)
Macleod Football Club – Founded in 1946 (before 1950)
Montmorency Football Club – Founded in 1924 (before 1950)
North Heidelberg Football Club – Founded in 1958 (not before 1950)
Northcote Park Football Club – Founded in 1952 (not before 1950)
West Preston Lakeside Football Club – Founded in 1998 (not before 1950)
Correct count: The teams founded before 1950 are:
Eltham Football Club (1909)
Greensborough Football Club (1905)
Heidelberg Football Club (1876)
Macleod Football Club (1946)
Montmorency Football Club (1924)
So, there are 5 teams founded before 1950. The Prediction Answer should be YES.

Conclusion: [Incorrect]"""]

wrong_3 = ["""Original Table:
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

Statement:
the average score of all home team members for all dates is 2.125

Prediction Answer:
YES

Explanation: To calculate the average score of all home team members, we need to sum up the scores for the home teams and divide by the total number of home teams listed.
Here are the scores for the home teams from the table:
Foolad: 4
Rah Ahan: 2
Zob Ahan: 1
Bargh Shiraz: 1
Shahin Bushehr: 2
Pas Hamedan: 3
Moghavemat Sepasi: 1
Sanaye Arak: 0
The total score is 4+2+1+1+2+3+1+0=144 + 2 + 1 + 1 + 2 + 3 + 1 + 0 = 144+2+1+1+2+3+1+0=14.
There are 8 home teams in total.
Therefore, the average score is 1.75.
So the Prediction Answer YES is incorrect.

Conclusion: [Incorrect]"""]

if __name__=="__main__":
    data_dict = {
        "correct_3":correct_2,
        "incorrect_1":wrong_1,
        "correct_1":correct_1,
        "incorrect_2":wrong_2,
        "correct_3":correct_3,
        "incorrect_3":wrong_3,
    }
    file_path = "critic/TableFV/tools/few_shot_judge.json"

    with open(file_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)