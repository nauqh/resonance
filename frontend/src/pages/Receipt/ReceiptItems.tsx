import "./Receipt.css";

interface Item {
	name: string;
	artist: string;
	duration: string;
}

interface ReceiptItemsProps {
	items: Item[];
}

export const calculateDuration = (items: Item[]): string => {
	const totalSeconds = items.reduce((total, item) => {
		const [minutes, seconds] = item.duration.split(":").map(Number);
		return total + minutes * 60 + seconds;
	}, 0);

	const minutes = Math.floor(totalSeconds / 60);
	const formattedSeconds = (totalSeconds % 60).toString().padStart(2, "0");

	return `${minutes}:${formattedSeconds}`;
};

const ReceiptItems = ({ items }: ReceiptItemsProps) => {
	return (
		<tbody>
			{items.map((item, index) => (
				<tr key={index}>
					<td>{index + 1}</td>
					<td>
						{item.name} - {item.artist}
					</td>
					<td>{item.duration}</td>
				</tr>
			))}
		</tbody>
	);
};

export default ReceiptItems;
