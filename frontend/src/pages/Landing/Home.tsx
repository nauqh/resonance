import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ScrollReveal from "scrollreveal";
import Footer from "../../components/Footer";

import "./Home.css";

const sr = ScrollReveal({
	duration: 3000,
});

const Home = () => {
	const [playlistLink, setPlaylistLink] = useState("");
	const navigate = useNavigate();

	const [title, setTitle] = useState("How sick is your music?");

	useEffect(() => {
		function handleResize() {
			if (window.innerWidth < 500) {
				setTitle("Musicotherapy");
			} else {
				setTitle("How sick is your music?");
			}
		}

		window.addEventListener("resize", handleResize);
		return () => {
			window.removeEventListener("resize", handleResize);
		};
	}, []);

	useEffect(() => {
		sr.reveal(`.home__data`, { origin: "top", delay: 100 });
		sr.reveal(`.home__img`, { origin: "bottom", delay: 200 });
		sr.reveal(`.home__footer`, { delay: 800 });
	}, []);

	const handleButtonClick = () => {
		if (playlistLink.startsWith("https://")) {
			window.location.href = "https://resonances.streamlit.app/";
		} else {
			navigate("/input", {
				state: { link: playlistLink },
			});
		}
	};

	return (
		<>
			<section className="home">
				<div className="home__container container">
					<div className="home__data">
						<h1 className="home__title">{title}</h1>
						<p className="home__description">
							Our sophisticated AI diagnoses and prescribes
							awesome remedies for that awful music taste of
							yours.
						</p>

						<div className="button-container">
							<a className="button" onClick={handleButtonClick}>
								Find out
							</a>
							<a
								href="https://github.com/nauqh/resonance"
								target="_blank"
								className="button-alter"
							>
								Learn more
							</a>
						</div>

						<div className="home__input">
							<p className="home__description">
								Or upload your Spotify playlist below
							</p>
							<div className="input-container">
								<form action="">
									<input
										type="text"
										id="lname"
										name="lname"
										placeholder="Insert Spotify playlist link here"
										onChange={(e) =>
											setPlaylistLink(e.target.value)
										}
									/>
								</form>
							</div>
						</div>
					</div>

					<div className="home__img">
						<img src="/vinyl.jpeg" alt="" />
						<div className="home__shadow"></div>
					</div>
				</div>

				<Footer />
			</section>
		</>
	);
};

export default Home;
