import { useRef } from "react";
import ReceiptItems from "./ReceiptItems";
import html2canvas from "html2canvas";

import "./Receipt.css";

interface Artist {
	name: string;
	img: string;
	id: string;
	content: string;
}

interface ReceiptProps {
	data: {
		genre: string;
		mood: string;
		color: string;
		characteristics: string[];
		artists: Artist[];
		tracks: {
			id: string;
			name: string;
			artist: string;
			duration: string;
		}[];
		playlist: any;
	};
}

const Receipt = (data: ReceiptProps) => {
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

	return (
		<>
			<div className="receipt__container" ref={containerRef}>
				<div className="receipt_header">
					<h1>Musicotherapy</h1>
					<h2>GENRE: {data.data.genre}</h2>
					<h2>MOOD: {data.data.mood}</h2>
					<h2>
						ARTISTS:{" "}
						{data.data.artists
							.map((artist) => artist.name)
							.join(", ")}
					</h2>
					<p className="description">
						{data.data.characteristics[0]}
					</p>
				</div>

				<div className="receipt_body">
					<h2>
						ALBUM:{" "}
						<a href={data.data.playlist.external_urls.spotify}>
							{data.data.playlist.name}
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
							<ReceiptItems items={data.data.tracks} />
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
