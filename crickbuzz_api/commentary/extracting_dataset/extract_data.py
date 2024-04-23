import os
import json
import time
import pandas as pd
import re

def get_match_ids():
    match_ids = []
    f = open("/Users/aishwaryaravichandran/Downloads/crickbuzz_api/commentary/api/matches.json", "r")
    match_data = json.loads(f.read())
    for match_detail in match_data["matchDetails"]:
        match_detail_map = match_detail.get("matchDetailsMap", None)
        if match_detail_map:
            for match in match_detail_map["match"]:
                match_ids.append(match["matchInfo"]["matchId"])
    f.close()
    return match_ids

def load_json_files(file_path,match_id):
            
    # Open and read the JSON file
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    return json_data

def extract_commentary(json_data, match_id):

    data = [{"over_number": obj["overNumber"] if "overNumber" in obj else None, "commentary_data": obj["commText"], "timestamp": obj["timestamp"],} for obj in json_data]

    data = sorted(data, key=lambda x: x["timestamp"])

    df = pd.DataFrame(data)

    df['match_id'] = match_id

    set_preview(df)

    set_post(df)

    set_extra_overs(df)

    remove_noise(df)

    df.to_csv(f"/Users/aishwaryaravichandran/Downloads/crickbuzz_api/commentary/dataset/{match_id}/{match_id}_commentary.csv", index=False)

def set_preview(df):

    given_index = df["over_number"].first_valid_index()

    df.loc[:given_index - 1, "over_number"] = "preview"

    return df

def set_post(df):

    index = df["over_number"].last_valid_index()

    df.loc[index + 1:, "over_number"] = "post"

    return df

def set_extra_overs(df):

    none_indices = df.index[df["over_number"].isnull()]

    for none_index in none_indices:
        prev_non_none_index = df.loc[:none_index, "over_number"].last_valid_index()
        if prev_non_none_index is not None:
            df.at[none_index, "over_number"] = df.at[prev_non_none_index, "over_number"]

    return df

def remove_noise(df):

    pattern_1 = r'\b\d{1,2}\.\d{2}\s*(?:AM|PM)?\b'

    df['commentary_data'] = df['commentary_data'].str.replace(pattern_1, '', regex=True)

    pattern_2 = r'\bB\S*\:'

    df['commentary_data'] = df['commentary_data'].str.replace(pattern_2, '', regex=True)

    pattern_3 = r'\bB\S*\$'

    df['commentary_data'] = df['commentary_data'].str.replace(pattern_3, '', regex=True)

    pattern_4 = r'@'

    df['commentary_data'] = df['commentary_data'].str.replace(pattern_4, '', regex=True)

    pattern_5 = r'.*\\n.*'

    df['commentary_data'] = df['commentary_data'].str.replace(pattern_5, '', regex=True)

    df = df.dropna(subset=['commentary_data'])
    
def extract_highlights(highlights_json_data_1, highlights_json_data_2, match_id):

    data_1 = [{"over_number": obj["overNumber"] if "overNumber" in obj else None, "commentary_data": obj["commText"], "timestamp": obj["timestamp"]} for obj in highlights_json_data_1]

    data_1 = sorted(data_1, key=lambda x: x["timestamp"])

    df1 = pd.DataFrame(data_1)

    data_2 = [{"over_number": obj["overNumber"] if "overNumber" in obj else None, "commentary_data": obj["commText"], "timestamp": obj["timestamp"]} for obj in highlights_json_data_2]

    data_2 = sorted(data_2, key=lambda x: x["timestamp"])

    df2 = pd.DataFrame(data_2)

    appended_df = pd.concat([df1, df2], ignore_index=True)

    remove_noise(appended_df)

    appended_df.to_csv(f"/Users/aishwaryaravichandran/Downloads/crickbuzz_api/commentary/dataset/{match_id}/{match_id}_highlights.csv", index=False)

def extract_match_info(json_data, match_id):

    match_data = {
    "match_id": [json_data["matchInfo"]["matchId"]],
    "match_description": [json_data["matchInfo"]["matchDescription"]],
    "match_format": [json_data["matchInfo"]["matchFormat"]],
    "match_type": [json_data["matchInfo"]["matchType"]],
    "year": [json_data["matchInfo"]["year"]],
    "team1": [json_data["matchInfo"]["team1"]["name"]],
    "team2": [json_data["matchInfo"]["team2"]["name"]],
    "venue": [json_data["venueInfo"]["knownAs"]],
    "city": [json_data["venueInfo"]["city"]],
}

    # Convert the dictionary to a DataFrame
    match_df = pd.DataFrame(match_data)

    match_df.to_csv(f"/Users/aishwaryaravichandran/Downloads/crickbuzz_api/commentary/dataset/{match_id}/{match_id}_match_info.csv", index=False)

def extract_scorecard(json_data, match_id):

    batId_list = []
    batName = []
    runs_list = []
    balls_list = []
    dots_list = []
    fours_list = []
    sixes_list = []
    strikeRate_list = []
    outDesc_list = []
    bowlerId_list = []
    wicketCode_list = []
    isOverseas_list = []

    batsmen_data = json_data["scoreCard"][0]["batTeamDetails"]["batsmenData"]
    for key, value in batsmen_data.items():
        bat_id = value["batId"]
        bat_name = value["batName"]
        runs = value["runs"]
        balls = value["balls"]
        dots = value["dots"]
        fours = value["fours"]
        sixes = value["sixes"]
        strikerate = value["strikeRate"]
        out_desc = value["outDesc"]
        bow_id = value["bowlerId"]
        wicket_code = value["wicketCode"]
        isOverseas = value["isOverseas"]


        batId_list.append(bat_id)
        batName.append(bat_name)
        runs_list.append(runs)
        balls_list.append(balls)
        dots_list.append(dots)
        fours_list.append(fours)
        sixes_list.append(sixes)
        strikeRate_list.append(strikerate)
        outDesc_list.append(out_desc)
        bowlerId_list.append(bow_id)
        wicketCode_list.append(wicket_code)
        isOverseas_list.append(isOverseas)

        scorecard_data = {
        "match_id": [json_data["scoreCard"][0]["matchId"]] * len(batId_list),
        "inning_id": [json_data["scoreCard"][0]["inningsId"]] * len(batId_list),
        "team_name": [json_data["scoreCard"][0]["batTeamDetails"]["batTeamName"]] * len(batId_list),
        "team_shortname": [json_data["scoreCard"][0]["batTeamDetails"]["batTeamShortName"]] * len(batId_list),
        "bat_id": batId_list,
        "bat_name": batName,
        "runs": runs_list,
        "balls": balls_list,
        "dots": dots_list,
        "fours": fours_list,
        "sixes": sixes_list,
        "strikeRate": strikeRate_list,
        "outDesc": outDesc_list,
        "bowlerId": bowlerId_list,
        "wicketCode": wicketCode_list,
        "isOverseas": isOverseas_list,
        }

    scorecard_data_df_1 = pd.DataFrame(scorecard_data)

    batsmen_data_1 = json_data["scoreCard"][1]["batTeamDetails"]["batsmenData"]

    batId_list = []
    batName = []
    runs_list = []
    balls_list = []
    dots_list = []
    fours_list = []
    sixes_list = []
    strikeRate_list = []
    outDesc_list = []
    bowlerId_list = []
    wicketCode_list = []
    isOverseas_list = []

    for key, value in batsmen_data_1.items():
        bat_id = value["batId"]
        bat_name = value["batName"]
        runs = value["runs"]
        balls = value["balls"]
        dots = value["dots"]
        fours = value["fours"]
        sixes = value["sixes"]
        strikerate = value["strikeRate"]
        out_desc = value["outDesc"]
        bow_id = value["bowlerId"]
        wicket_code = value["wicketCode"]
        isOverseas = value["isOverseas"]


        batId_list.append(bat_id)
        batName.append(bat_name)
        runs_list.append(runs)
        balls_list.append(balls)
        dots_list.append(dots)
        fours_list.append(fours)
        sixes_list.append(sixes)
        strikeRate_list.append(strikerate)
        outDesc_list.append(out_desc)
        bowlerId_list.append(bow_id)
        wicketCode_list.append(wicket_code)
        isOverseas_list.append(isOverseas)

    scorecard_data_2 = {
    "match_id": [json_data["scoreCard"][1]["matchId"]] * len(batId_list),
    "inning_id": [json_data["scoreCard"][1]["inningsId"]] * len(batId_list),
    "team_name": [json_data["scoreCard"][1]["batTeamDetails"]["batTeamName"]] * len(batId_list),
    "team_shortname": [json_data["scoreCard"][1]["batTeamDetails"]["batTeamShortName"]] * len(batId_list),
    "bat_id": batId_list,
    "bat_name": batName,
    "runs": runs_list,
    "balls": balls_list,
    "dots": dots_list,
    "fours": fours_list,
    "sixes": sixes_list,
    "strikeRate": strikeRate_list,
    "outDesc": outDesc_list,
    "bowlerId": bowlerId_list,
    "wicketCode": wicketCode_list,
    "isOverseas": isOverseas_list,
    }

    scorecard_data_df_2 = pd.DataFrame(scorecard_data_2)

    appended_df = pd.concat([scorecard_data_df_1, scorecard_data_df_2], ignore_index=True)

    appended_df.to_csv(f"/Users/aishwaryaravichandran/Downloads/crickbuzz_api/commentary/dataset/{match_id}/{match_id}_match_info_batting.csv", index=False)

    bowlerId_list = []
    bowlName_list = []
    overs_list = []
    maiden_list = []
    runs_list = []
    dots_list = []
    wickets_list = []
    economy_list = []
    no_balls_list = []
    wides_list = []
    isOverseas_list = []

    bowling_data = json_data["scoreCard"][0]["bowlTeamDetails"]["bowlersData"]
    for key, value in bowling_data.items():
        bow_id = value["bowlerId"]
        bow_name = value["bowlName"]
        overs = value["overs"]
        maidens = value["maidens"]
        runs = value["runs"]
        dots = value["dots"]
        wickets = value["wickets"]
        economy = value["economy"]
        no_balls = value["no_balls"]
        wides = value["wides"]
        isOverseas = value["isOverseas"]


        bowlerId_list.append(bow_id)
        bowlName_list.append(bow_name)
        overs_list.append(overs)
        maiden_list.append(maidens)
        runs_list.append(runs)
        dots_list.append(dots)
        wickets_list.append(wickets)
        economy_list.append(economy)
        no_balls_list.append(no_balls)
        wides_list.append(wides)
        isOverseas_list.append(isOverseas)

    scorecard_data_3 = {
    "match_id": [json_data["scoreCard"][0]["matchId"]] * len(bowlerId_list),
    "inning_id": [json_data["scoreCard"][0]["inningsId"]] * len(bowlerId_list),
    "team_name": [json_data["scoreCard"][0]["bowlTeamDetails"]["bowlTeamName"]] * len(bowlerId_list),
    "team_shortname": [json_data["scoreCard"][0]["bowlTeamDetails"]["bowlTeamShortName"]] * len(bowlerId_list),
    "bowl_id": bowlerId_list,
    "bowl_name": bowlName_list,
    "overs": overs_list,
    "maidens": maiden_list,
    "runs": runs_list,
    "dots": dots_list,
    "wickets": wickets_list,
    "economy": economy_list,
    "no_balls": no_balls_list,
    "wides": wides_list,
    "isOverseas": isOverseas_list,
    }

    scorecard_data_df_3 = pd.DataFrame(scorecard_data_3)

    bowlerId_list = []
    bowlName_list = []
    overs_list = []
    maiden_list = []
    runs_list = []
    dots_list = []
    wickets_list = []
    economy_list = []
    no_balls_list = []
    wides_list = []
    isOverseas_list = []

    bowling_data_2 = json_data["scoreCard"][1]["bowlTeamDetails"]["bowlersData"]
    for key, value in bowling_data.items():
        bow_id = value["bowlerId"]
        bow_name = value["bowlName"]
        overs = value["overs"]
        maidens = value["maidens"]
        runs = value["runs"]
        dots = value["dots"]
        wickets = value["wickets"]
        economy = value["economy"]
        no_balls = value["no_balls"]
        wides = value["wides"]
        isOverseas = value["isOverseas"]


        bowlerId_list.append(bow_id)
        bowlName_list.append(bow_name)
        overs_list.append(overs)
        maiden_list.append(maidens)
        runs_list.append(runs)
        dots_list.append(dots)
        wickets_list.append(wickets)
        economy_list.append(economy)
        no_balls_list.append(no_balls)
        wides_list.append(wides)
        isOverseas_list.append(isOverseas)

    scorecard_data_4 = {
    "match_id": [json_data["scoreCard"][1]["matchId"]] * len(bowlerId_list),
    "inning_id": [json_data["scoreCard"][1]["inningsId"]] * len(bowlerId_list),
    "team_name": [json_data["scoreCard"][1]["bowlTeamDetails"]["bowlTeamName"]] * len(bowlerId_list),
    "team_shortname": [json_data["scoreCard"][1]["bowlTeamDetails"]["bowlTeamShortName"]] * len(bowlerId_list),
    "bowl_id": bowlerId_list,
    "bowl_name": bowlName_list,
    "overs": overs_list,
    "maidens": maiden_list,
    "runs": runs_list,
    "dots": dots_list,
    "wickets": wickets_list,
    "economy": economy_list,
    "no_balls": no_balls_list,
    "wides": wides_list,
    "isOverseas": isOverseas_list,
    }

    scorecard_data_df_4 = pd.DataFrame(scorecard_data_4)

    appended_df_2 = pd.concat([scorecard_data_df_3, scorecard_data_df_4], ignore_index=True)

    appended_df_2.to_csv(f"/Users/aishwaryaravichandran/Downloads/crickbuzz_api/commentary/dataset/{match_id}/{match_id}_match_info_bowling.csv", index=False)

def main():

    # gets the match ids from the file generated in previous step
    match_ids = get_match_ids() 

    i = 0
    for match_id in match_ids:
        if(i < 30):
            commentary_folder_path = f"/Users/aishwaryaravichandran/Downloads/crickbuzz_api/commentary/api/commentary_data/{match_id}.json"
            commentart_json_data = load_json_files(commentary_folder_path,match_id)
            extract_commentary(commentart_json_data, match_id)
            time.sleep(1)

            highlights_folder_path_1 = f"/Users/aishwaryaravichandran/Downloads/crickbuzz_api/commentary/api/highlights/1st/{match_id}.json"
            highlights_json_data_1 = load_json_files(highlights_folder_path_1,match_id)
            highlights_folder_path_2 = f"/Users/aishwaryaravichandran/Downloads/crickbuzz_api/commentary/api/highlights/2nd/{match_id}.json"
            highlights_json_data_2 = load_json_files(highlights_folder_path_2,match_id)
            extract_highlights(highlights_json_data_1, highlights_json_data_2, match_id)
            time.sleep(1)

            match_info_folder_path = f"/Users/aishwaryaravichandran/Downloads/crickbuzz_api/commentary/api/match_info/{match_id}.json"
            match_info_json_data = load_json_files(match_info_folder_path,match_id)
            extract_match_info(match_info_json_data, match_id)
            time.sleep(1)

            scorecard_folder_path = f"/Users/aishwaryaravichandran/Downloads/crickbuzz_api/commentary/api/scorecard/{match_id}.json"
            scorecard_json_data = load_json_files(scorecard_folder_path,match_id)
            extract_scorecard(scorecard_json_data, match_id)
            time.sleep(1)

            i += 1

if __name__ == "__main__":
    main()