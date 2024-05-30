const Footer = () => {
	return (
		<footer className="home__footer">
			<div>
				A project by{" "}
				<span style={{ fontSize: "2rem", fontWeight: 700 }}>
					<a href="https://nauqh.github.io">Nauqh</a>
				</span>
			</div>
			<span
				style={{
					alignSelf: "flex-end",
					textAlign: "right",
					width: 200,
				}}
			>
				Powered by{" "}
				<a href="https://openai.com/blog/new-embedding-models-and-api-updates">
					OpenAI GPT-4
				</a>
			</span>
		</footer>
	);
};

export default Footer;
