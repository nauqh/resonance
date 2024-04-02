interface GenreGridProps {
	onDiagnoseSelect: (text: string) => void;
}

const genres = [
	{ name: "Pop Punk" },
	{ name: "Korean Soft Indie", className: "grid-3" },
	{ name: "R&B" },
	{ name: "Lo-fi" },
	{ name: "Rap Hip-hop", className: "grid-2" },
	{ name: "Disney Soundtracks", className: "grid-2" },
	{ name: "EDM" },
	{ name: "Mandopop" },
	{ name: "Classical" },
	{ name: "Reggaeton", className: "grid-2" },
	{ name: "Pop Ballad" },
];

const GenreGrid = ({ onDiagnoseSelect }: GenreGridProps) => {
	return (
		<div className="container-grid">
			{genres.map((genre, index) => (
				<div
					key={index}
					className={`button-brick ${
						genre.className ? genre.className : ""
					}`}
					onClick={() => onDiagnoseSelect(genre.name)}
				>
					<span>{genre.name}</span>
				</div>
			))}
		</div>
	);
};

export default GenreGrid;
