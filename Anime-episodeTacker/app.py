from flask import Flask
import csv

app = Flask(__name__)

FILE_NAME = "anime_list.csv"

def load_anime_list():
    "Read CSV and return list of dicts"
    anime_list = []
    with open(FILE_NAME, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['total_episodes'] = int(row['total_episodes'])
            row['watched_episodes'] = int(row['watched_episodes'])
            anime_list.append(row)

    return anime_list

@app.route("/")
def index():
    anime_list = load_anime_list()

    #Build HTML rows dynamically from CSV data
    rows = ''
    for i, anime in enumerate(anime_list, start=1):
        remaining = anime["total_episodes"] - anime['watched_episodes']
        rows += f"""
        <tr>
            <td>{i}</td>
            <td>{anime['title']}</td>
            <td>{anime['watched_episodes']}/{anime['total_episodes']}</td>
            <td>{remaining}</td>
            <td>{anime['status']}</td>
        </tr>
        """

    #Full HTML page as a string
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Anime Tacker</title>
        <style>
            body {{font-family: Arial; padding: 30px; background: #1a1a2e; color: white; }}
            h1 {{ color: #e94560; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th {{ background: #0f3460; padding: 10px; border-bottom: 1px solid #333; text-align: left; }}

            tr:hover {{ background: #16213e; }}
        </style>
    </head>
    <body>
        <h1>My Anime</h1>
        <p>Total: {len(anime_list)} anime</p>
        <table>
            <tr>
                <th>#</th>
                <th>Title</th>
                <th>Progress</th>
                <th>Remaining</th>
                <th>Status</th>
            <tr>
            {rows}
        </table>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    app.run(debug=True)

