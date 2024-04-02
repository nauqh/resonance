import "./Playlist.css";

interface PlaylistProps {
	playlist: any;
	color: any;
}

const Playlist = ({ playlist, color }: PlaylistProps) => {
	return (
		<div className="playlist__container">
			<iframe
				src={`https://open.spotify.com/embed/playlist/${playlist.id}?utm_source=generator`}
				frameBorder="0"
				allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
				loading="lazy"
			></iframe>
			<div className="playlist__description">
				<div className="playlist__description-head">
					<h5>PUBLIC PLAYLIST</h5>
					<h1 style={{ color: color }}>{playlist.name}</h1>
					<p>
						{playlist.description
							? playlist.description
							: `Yet to have description`}
					</p>
				</div>
				<div className="playlist__description-stats">
					<h3>
						<span
							style={{
								color: color,
							}}
						>
							Owner
						</span>
						: {playlist.owner.display_name}
					</h3>
					<h3>
						<span
							style={{
								color: color,
							}}
						>
							Content
						</span>
						: {playlist.tracks.total} tracks
					</h3>
					<h3>
						<span
							style={{
								color: color,
							}}
						>
							Duration
						</span>
						: 12h
					</h3>
				</div>
			</div>
		</div>
	);
};

export default Playlist;
