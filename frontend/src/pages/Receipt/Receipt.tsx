import { useRef } from "react";
import ReceiptItems, { calculateDuration } from "./ReceiptItems";
import html2canvas from "html2canvas";
import { Toaster, toast } from "sonner";

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
	};
	playlist: any;
}

const Receipt = ({ data, playlist }: ReceiptProps) => {
	const containerRef = useRef(null);

	const handleScreenshot = () => {
		const container = containerRef.current;
		if (!container) return;

		html2canvas(container).then((canvas) => {
			const a = document.createElement("a");
			a.href = canvas.toDataURL("image/png");
			a.download = "receipt.png";
			a.click();
		});
	};

	const handleEmailReceipt = () => {
		const container = containerRef.current;
		if (!container) return;

		html2canvas(container).then((canvas) => {
			const postData = {
				recipients: ["quan.do@coderschool.vn"],
				attachment: canvas.toDataURL("image/png"),
			};

			fetch("http://127.0.0.1:8000/receipt", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(postData),
			}).then((response) => {
				if (!response.ok) {
					throw new Error("Failed to send receipt.");
				}
				toast.success("Receipt has been sent");
			});
		});
	};

	const { genre, mood, characteristics, artists, tracks } = data;

	return (
		<div className="receipt__flex">
			<div className="receipt__container" ref={containerRef}>
				<div className="receipt_header">
					<h1>Musicotherapy</h1>
					<h2>GENRE: {genre}</h2>
					<h2>MOOD: {mood}</h2>
					<h2>
						ARTISTS:{" "}
						{artists.map((artist) => artist.name).join(", ")}
					</h2>
					<p className="description">{characteristics[0]}</p>
				</div>

				<div className="receipt_body">
					<h2>
						ALBUM:{" "}
						<a href={playlist.external_urls.spotify}>
							{playlist.name}
						</a>
					</h2>

					<h2>PRESCRIPTION: </h2>

					<div className="items">
						<table>
							<thead>
								<tr>
									<th>QTY</th>
									<th>ITEM</th>
									<th>AMT</th>
								</tr>
							</thead>
							<ReceiptItems items={tracks} />
						</table>
					</div>
				</div>

				<table>
					<tfoot>
						<tr>
							<td>TREATMENTS:</td>
							<td>9</td>
						</tr>
						<tr>
							<td>SESSION DURATION:</td>
							<td>{calculateDuration(tracks)}</td>
						</tr>
					</tfoot>
				</table>

				<div className="receipt__additional">
					<h2>
						CARD NAME: **** **** **** {new Date().getFullYear()}
					</h2>
				</div>

				<h3 className="receipt__footer">THANK YOU FOR VISITING</h3>
				<img className="receipt__img" src="/spotify_logo.png" alt="" />
			</div>

			<div className="receipt__button-container">
				<button
					className="button-alter"
					style={{ fontSize: "1rem" }}
					onClick={handleScreenshot}
				>
					Download receipt
				</button>

				<button
					className="button-alter"
					style={{ fontSize: "1rem" }}
					onClick={() =>
						(window.location.href =
							"https://musicotherapy.vercel.app/")
					}
				>
					New Diagnosis
				</button>
			</div>

			<Toaster
				toastOptions={{
					style: { background: "#fafafa" },
				}}
				position="bottom-center"
			/>
		</div>
	);
};

export default Receipt;
