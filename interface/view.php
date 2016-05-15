<?php
$servername = "localhost";
$username = "euro";
$password = "2016";
$dbname = "euro2016";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

# parameters

#event_id
#timestamp
#event_name
#home_odds
#event_date
#away_odds
#draw_odds
    #select * from messages where id in (select max(id) from messages group by Name)
$sql_odds = "SELECT event_id, timestamp, event_name, home_odds, event_date, away_odds, draw_odds FROM euro_2016_betfair where timestamp in ( select max(timestamp) from euro_2016_betfair group by event_id) order by event_date";
$result_odds = $conn->query($sql_odds);

$sql_last_hr = "SELECT event_id, timestamp, event_name, home_odds, event_date, away_odds, draw_odds FROM euro_2016_betfair where timestamp in ( select max(timestamp) from euro_2016_betfair group by event_id) order by event_date";
$result_last_hr = $conn->query($sql_last_hr);

if ($result_odds->num_rows > 0) {
    // output data of each row
    ?>
    <table>
        <table border="1">
     <tr>
         <td><b>Match Time</b></td><td><b>Match</b></td><td><b>Home (Odds/%)</b></td><td><b>Draw (Odds/%)</b></td><td><b>Away (Odds/%)</b></td><td><b>Overround</b></td><td><b>Last Update (BST)</b></td><td></td>  
     </tr>
        <?php
    while($row = $result_odds->fetch_assoc()) {
        echo "<tr>
        <td>".$row["event_date"]." </td>
        <td>".$row["event_name"]." </td>
            <td>".$row["home_odds"]."&nbsp;&nbsp;/&nbsp;&nbsp; <i>".round((100/$row["home_odds"])/(1/$row["away_odds"]+1/$row["home_odds"]+1/$row["draw_odds"]),2)."%</i> </td>
                <td>".$row["draw_odds"]."&nbsp;&nbsp;/&nbsp;&nbsp; <i>".round((100/$row["draw_odds"])/(1/$row["away_odds"]+1/$row["home_odds"]+1/$row["draw_odds"]),2)."%</i> </td>
                <td>".$row["away_odds"]."&nbsp;&nbsp;/&nbsp;&nbsp; <i>".round((100/$row["away_odds"])/(1/$row["away_odds"]+1/$row["home_odds"]+1/$row["draw_odds"]),2)."%</i> </td>
                <td><i>".round((100/$row["away_odds"]+100/$row["home_odds"]+100/$row["draw_odds"]),2)."%</i></td>
                <td><i>".$row["timestamp"]." </i></td><td>"."<a href='https://www.betfair.com/exchange/football/event?id=".$row["event_id"]."'>bet</a></td>
                </tr>";
      # overround
      #(1/$row["away_odds"]+1/$row["home_odds"]+1/$row["draw_odds"])
    }
     echo "</table>";
} else {
    echo "0 results";
}
$conn->close();
?>