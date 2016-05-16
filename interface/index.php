<head>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<?php include_once("tracking.php") ?>

<h2>Euro 2016 Odds Analysis</h2>
		
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
?>
<div style='background-color:white;width:1000px; margin:0 auto;padding:10px'>
	<div align="center"
		<table style='background-color:#33cc33;border:1px solid black;'>
		<tr> <td><b>Cells in green</b></td> </tr>
		</table>
	</div>
	 indicate markets on betfair which <i>might</i> be worth betting against, according to an analysis of the <a href="http://www.eloratings.net/">ELO ratings</a> of the teams. Currently, differences of more than 10% are highlighted<br/><br/> 
The implied probabilities from the latest odds from the betfair exchange (left column, 'Bet %') are compared with the model estimate (right column, 'OA %') for each outcome. The betting probabilities are normalised for the <a href="https://en.wikipedia.org/wiki/Mathematics_of_bookmaking#Making_a_.27book.27_.28and_the_notion_of_overround.29">overround</a>.
<br/><br/>Draw probabilities have been estimated from a comparison of draw frequency at major tournaments with the rating differential.

	</div>
	<?php	
$sql_odds = "SELECT * FROM euro_2016_analysis where timestamp in ( select max(timestamp) from euro_2016_analysis group by event_id) order by event_date";
$result_odds = $conn->query($sql_odds);

if ($result_odds->num_rows > 0) {
    ?>
<div class="wrapper">
    <div class="table">
         <div class="row header">
					<div class="cell">Match Time</div>
					<div class="cell">Match</div>
					<div class="cell">Home</div>
					 <div class="cell"></div>
					<div class="cell">Draw</div>
					 <div class="cell"></div>
					<div class="cell">Away</div>
					 <div class="cell"></div>
					<div class="cell">Update (GMT+1)</div>
					 <div class="cell"></div>
     </div>
			    <div class="row header">
					<div class="cell"></div>
					<div class="cell"></div>
					<div class="cell">Bet %</div>
					<div class="cell">OA %</div>
					<div class="cell">Bet %</div>
					<div class="cell">OA %</div>
					<div class="cell">Bet %</div>
					<div class="cell">OA %</div> 
				 <div class="cell"></div>
						<div class="cell"></div>
     </div>
        <?php
	
    while($row = $result_odds->fetch_assoc()) {
		
        echo "<div class='row'>
        <div class='cell'>".$row["event_date"]." </div>
				<div class='cell'>".$row["home_team"]." v ".$row["away_team"]." </div>
          <div class='cell'>".round($row["odds_home_prob"]*100,1)."%</div>";
					
			# HOME
			if (sqrt(($row["calc_home_prob"]-$row["odds_home_prob"])*($row["calc_home_prob"]-$row["odds_home_prob"]))>0.1){
					echo "<div class='cell' style='background-color:#33cc33;border:1px solid black;'><b>".round($row["calc_home_prob"]*100,2)."%</b></div>";
			}
			else{ 
					echo "<div class='cell'><b>".round($row["calc_home_prob"]*100,2)."%</b></div>";
			}
			
			# DRAW
			echo "<div class='cell'>".round($row["odds_draw_prob"]*100,1)."%</div>";	
			
			if (sqrt(($row["calc_draw_prob"]-$row["odds_draw_prob"])*($row["calc_draw_prob"]-$row["odds_draw_prob"]))>0.1){
						echo "<div class='cell' style='background-color:#33cc33;border:1px solid black;'><b>".round($row["calc_draw_prob"]*100,2)."%</b></div>";
			}
			else{ 
				echo "<div class='cell'><b>".round($row["calc_draw_prob"]*100,2)."%</b></div>";
			}
			
			#AWAY
			echo "<div class='cell'>".round($row["odds_away_prob"]*100,1)."%</div>";
			
			if (sqrt(($row["calc_away_prob"]-$row["odds_away_prob"])*($row["calc_away_prob"]-$row["odds_away_prob"]))>0.1){
					  echo "<div class='cell' style='background-color:#33cc33;border:1px solid black;'><b>".round($row["calc_away_prob"]*100,2)."%</b></div>";
			}
			else{
				echo "<div class='cell'><b>".round($row["calc_away_prob"]*100,2)."%</b></div>";			
			}
			
			echo "<div class='cell'><i>".$row["timestamp"]." </i></div> <div class='cell'><a href='https://www.betfair.com/exchange/football/event?id=".$row["event_id"]."'>Betfair</a></div>";
			
			# end of row div
			echo "</div>";
    }
	# end of table div
     echo "</div>";
} else {
    echo "0 results";
}
$conn->close();
?>
</body>
