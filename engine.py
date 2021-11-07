import pandas as pd
import requests
import json
from math import ceil
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "environment.env")
load_dotenv(dotenv_path)


API_KEY = os.environ["API_KEY"]


def get_channel_id_from_url(url):
    channel_id = list(filter(lambda x: x != "", url.split("/")))
    return channel_id[-1] if id else None


def get_channel_info_meta(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&key={API_KEY}&id={channel_id}"
    channel_info = requests.get(url)
    json_data = json.loads(channel_info.text)
    return json_data


def get_video_id_and_playlist_id(
    channel_id, no_of_page, max_record_in_page=50
):
    video_ids, playlist_ids = [], []
    next_page_token = ""
    for each_page in range(no_of_page):
        if next_page_token != None:
            url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&part=snippet&channelId={channel_id}&maxResults={max_record_in_page}&pageToken={next_page_token}"
        data = json.loads(requests.get(url).text)
        if "items" in data:
            for item in data["items"]:
                if item["id"]["kind"] == "youtube#video":
                    video_ids.append(item["id"]["videoId"])
                elif item["id"]["kind"] == "youtube#playlist":
                    playlist_ids.append(item["id"]["playlistId"])
        next_page_token = (
            data["nextPageToken"] if "nextPageToken" in data else None
        )
    return (video_ids, playlist_ids)


def construct_df_of_video_details(video_ids):
    df = pd.DataFrame(
        columns=[
            "video_id",
            "published_at",
            "video_title",
            "view_count",
            "like_count",
            "dislike_count",
            "comment_count",
            "favorite_count",
            "video_duration",
            "caption",
        ]
    )
    for index, video_id in enumerate(video_ids):
        url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet,contentDetails&key={API_KEY}&id={video_id}"
        data = json.loads(requests.get(url).text)
        published_at = data["items"][0]["snippet"]["publishedAt"]
        video_title = data["items"][0]["snippet"]["title"]
        view_count = int(data["items"][0]["statistics"]["viewCount"])
        like_count = int(data["items"][0]["statistics"]["likeCount"])
        dislike_count = int(data["items"][0]["statistics"]["dislikeCount"])
        comment_count = int(data["items"][0]["statistics"]["commentCount"])
        favorite_count = int(data["items"][0]["statistics"]["favoriteCount"])
        video_duration = data["items"][0]["contentDetails"]["duration"]
        caption = data["items"][0]["contentDetails"]["caption"]
        video_detail = [
            video_id,
            published_at,
            video_title,
            view_count,
            like_count,
            dislike_count,
            comment_count,
            favorite_count,
            video_duration,
            caption,
        ]
        df.loc[index] = video_detail
    return df


def construct_result_dict_from_frame(df):
    # final_dict = {}
    # final_dict["total_views"] = df["view_count"].sum()
    # final_dict["total_likes"] = df["like_count"].sum()
    # final_dict["total_dislikes"] = df["dislike_count"].sum()
    # final_dict["total_comments"] = df["comment_count"].sum()
    # final_dict["total_favorites"] = df["favorite_count"].sum()
    # final_dict["average_views"] = df["view_count"].mean()
    # final_dict["average_likes"] = df["like_count"].mean()
    # final_dict["average_dislikes"] = df["dislike_count"].mean()
    # final_dict["average_comments"] = df["comment_count"].mean()
    # final_dict["average_favorites"] = df["favorite_count"].mean()
    # final_dict["max_view_for_video"] = df["view_count"].max()
    # final_dict["max_like_for_video"] = df["like_count"].max()
    # final_dict["max_dislike_for_video"] = df["dislike_count"].max()
    # final_dict["max_comment_for_video"] = df["comment_count"].max()
    # max_viewed_video_details = list(
    #     df.sort_values(by="view_count", ascending=False).iloc[0]
    # )
    # max_liked_video_details = list(
    #     df.sort_values(by="like_count", ascending=False).iloc[0]
    # )
    # max_disliked_video_details = list(
    #     df.sort_values(by="dislike_count", ascending=False).iloc[0]
    # )
    # max_commented_video_details = list(
    #     df.sort_values(by="comment_count", ascending=False).iloc[0]
    # )
    # final_dict["max_viewed_video"] = (
    #     "https://www.youtube.com/watch?v=" + max_viewed_video_details[0]
    # )
    # final_dict["max_liked_video"] = (
    #     "https://www.youtube.com/watch?v=" + max_liked_video_details[0]
    # )
    # final_dict["max_disliked_video"] = (
    #     "https://www.youtube.com/watch?v=" + max_disliked_video_details[0]
    # )
    # final_dict["max_commented_video"] = (
    #     "https://www.youtube.com/watch?v=" + max_commented_video_details[0]
    # )
    # final_dict["title_of_max_viewed_video"] = max_viewed_video_details[2]
    # final_dict["title_of_max_liked_video"] = max_liked_video_details[2]
    # final_dict["title_of_max_disliked_video"] = max_disliked_video_details[2]
    # final_dict["title_of_max_commented_video"] = max_commented_video_details[2]

    final_list = []
    max_viewed_video_details = list(
        df.sort_values(by="view_count", ascending=False).iloc[0]
    )
    max_liked_video_details = list(
        df.sort_values(by="like_count", ascending=False).iloc[0]
    )
    max_disliked_video_details = list(
        df.sort_values(by="dislike_count", ascending=False).iloc[0]
    )
    max_commented_video_details = list(
        df.sort_values(by="comment_count", ascending=False).iloc[0]
    )
    final_list.append("Total Views : " + str(df["view_count"].sum()))
    final_list.append("Total Likes : " + str(df["like_count"].sum()))
    final_list.append("Total Dislikes : " + str(df["dislike_count"].sum()))
    final_list.append("Total Comments : " + str(df["comment_count"].sum()))
    final_list.append(
        "Average No.of. Views : " + str(int(df["view_count"].mean()))
    )
    final_list.append(
        "Average No.of. Likes : " + str(int(df["like_count"].mean()))
    )
    final_list.append(
        "Average No.of. Dislikes : " + str(int(df["dislike_count"].mean()))
    )
    final_list.append(
        "Average No.of. Comments : " + str(int(df["comment_count"].mean()))
    )

    final_list.append(
        "Maximum View for a video : " + str(df["view_count"].max())
    )
    final_list.append(
        "Maximum Viewed Video : "
        + "https://youtu.be/"
        + max_viewed_video_details[0]
    )
    final_list.append(
        "Title of Maximum Viewed Video : " + max_viewed_video_details[2]
    )

    final_list.append(
        "Maximum Like for a video : " + str(df["like_count"].max())
    )
    final_list.append(
        "Maximum Liked Video : "
        + "https://youtu.be/"
        + max_liked_video_details[0]
    )
    final_list.append(
        "Title of Maximum Liked Video : " + max_liked_video_details[2]
    )

    final_list.append(
        "Maximum Dislike for a video : " + str(df["dislike_count"].max())
    )
    final_list.append(
        "Maximum Disliked Video : "
        + "https://youtu.be/"
        + max_disliked_video_details[0]
    )
    final_list.append(
        "Title of Maximum Disliked Video : " + max_disliked_video_details[2]
    )

    final_list.append(
        "Maximum Comment for a video : " + str(df["comment_count"].max())
    )
    final_list.append(
        "Maximum Commented Video : "
        + "https://youtu.be/"
        + max_commented_video_details[0]
    )
    final_list.append(
        "Title of Maximum Commented Video : " + max_commented_video_details[2]
    )

    return final_list


def process_channel(url):
    print('requestURL',url)
    channel_id = get_channel_id_from_url(url)
    print('channelIDfromURL',channel_id)
    channel_info_meta = get_channel_info_meta(channel_id)
    print('channel_info_meta',channel_info_meta)
    if "items" not in channel_info_meta:
        return [
            "Please enter valid Channel URL. Eg: https://www.youtube.com/channel/UCsXVk37bltHxD1rDPwtNM8Q"
        ]
    no_of_page_to_call = int(
        ceil(
            int(channel_info_meta["items"][0]["statistics"]["videoCount"]) / 50
        )
    )
    video_ids, playlist_ids = get_video_id_and_playlist_id(
        channel_id, no_of_page_to_call
    )
    df = construct_df_of_video_details(video_ids)
    # df.to_csv('channel_details.csv', index=False)
    final_list = construct_result_dict_from_frame(df)
    return final_list
