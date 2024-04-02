import React from "react";

interface ArtistInfoProps {
	img: string;
	name: string;
	content: string;
	color: string;
}

const Artist: React.FC<ArtistInfoProps> = ({ img, name, content, color }) => {
	return (
		<div className="container-flex">
			<img src={img} width="200px" style={{ borderRadius: "0.5rem" }} />
			<p style={{ maxWidth: "450px", fontWeight: 400 }}>
				<span
					style={{
						fontSize: "1.5rem",
						color: color,
						fontWeight: 700,
					}}
				>
					{name}
				</span>{" "}
				{content}
			</p>
		</div>
	);
};

export default Artist;
