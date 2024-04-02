import "./Receipt.css";

interface Item {
	name: string;
	artist: string;
	duration: string;
}

interface ReceiptItemsProps {
	items: Item[];
}

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
