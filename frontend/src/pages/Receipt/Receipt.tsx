import { useRef } from "react";
import ReceiptItems from "./ReceiptItems";
import html2canvas from "html2canvas";

import "./Receipt.css";

const Receipt = () => {
	const containerRef = useRef(null);

	const handleScreenshot = () => {
		const container = containerRef.current;
		if (!container) return;

		html2canvas(container).then((canvas) => {
			const link = document.createElement("a");
			link.href = canvas.toDataURL("image/png");
			link.download = "receipt.png";
			link.click();
		});
	};

	const items = [
		{
			id: "7AeZrMqWWSyPWOuyLKylID",
			name: "I Still Miss You (Feat. 달, 김프로)",
			artist: "SUNNYSIDEMJ",
			duration: "2:58",
		},
		{
			id: "1ZnSDGtDDta9qFNGEVoZbo",
			name: "I Wanna Say To You",
			artist: "Suzy",
			duration: "3:27",
		},
		{
			id: "3B4AOfW6nDbCPb1pIEczJQ",
			name: "Tattoo",
			artist: "Jukjae",
			duration: "3:09",
		},
		{
			id: "0rQsWe9gi2zhNycexfuAUD",
			name: "I'll become your spring - Drama Version",
			artist: "Airman",
			duration: "3:08",
		},
		{
			id: "3SXg7A9M3pY2aWYdzQ0BMW",
			name: "Beautiful Moment",
			artist: "K.Will",
			duration: "3:59",
		},
		{
			id: "6e1jziK0mMytJvWit0W04d",
			name: "비행운",
			artist: "MoonMoon",
			duration: "2:59",
		},
		{
			id: "7gAcFTyzB81ACPs299HS4M",
			name: "Your sea (Acc ver.)",
			artist: "J_ust",
			duration: "3:17",
		},
		{
			id: "4W7MrbhSg8o2v5lBz0wLBV",
			name: "Like We Turn the pages (Remaster)",
			artist: "homezone",
			duration: "3:13",
		},
		{
			id: "1MXw9VhdrArQeGcPQy9A1v",
			name: "Good bye",
			artist: "HYOLYN",
			duration: "3:39",
		},
	];

	return (
		<>
			<div className="receipt__container" ref={containerRef}>
				<div className="receipt_header">
					<h1>Musicotherapy</h1>
					<h2>GENRE: Korean Indie Pop</h2>
					<h2>MOOD: Eclectic - Soothing - Vibrant</h2>
					<h2>ARTISTS: Zion.T, 10cm</h2>
					<p className="description">
						Your music taste may leans a bit towards Korean Indie
						Pop, which is known for its diverse mix of styles and
						influences. This genre often features a blend of
						traditional Korean musical elements with modern pop
						sensibilities, creating a sound that's both familiar and
						fresh.
					</p>
				</div>

				<div className="receipt_body">
					<h2>
						ALBUM:{" "}
						<a href="https://open.spotify.com/playlist/0d94FaVJFNNspToUDtZptD">
							soft & chill korean music
						</a>
					</h2>
					<h2>RECOMMENDATION: </h2>
					<div className="items">
						<table>
							<thead>
								<tr>
									<th>QTY</th>
									<th>ITEM</th>
									<th>AMT</th>
								</tr>
							</thead>
							<ReceiptItems items={items} />
						</table>
					</div>
				</div>

				<table>
					<tfoot>
						<tr>
							<td>ITEMS COUNT:</td>
							<td>32.1</td>
						</tr>
						<tr>
							<td>TOTAL:</td>
							<td>32.1</td>
						</tr>
					</tfoot>
				</table>

				<div className="receipt__additional">
					<h2>CARD NAME: **** **** **** 2024</h2>
				</div>

				<h3 className="receipt__footer">THANK YOU FOR VISITING</h3>
				<img className="receipt__img" src="/spotify_logo.png" alt="" />
			</div>
			<div className="receipt__button-container">
				<div className="button-alter" onClick={handleScreenshot}>
					Download receipt
				</div>
			</div>
		</>
	);
};

export default Receipt;
