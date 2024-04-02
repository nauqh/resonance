import { useEffect } from "react";
import "./WorkFilter.css";

type FilterKey = "Upbeat" | "Ambient" | "Anxious" | "Inspiring";

interface WorkFilterProps {
	onFilterChange: (filter: FilterKey) => void;
}

const WorkFilter = ({ onFilterChange }: WorkFilterProps) => {
	useEffect(() => {
		const linkWork = document.querySelectorAll(".work__item");

		function activeWork(this: HTMLElement) {
			linkWork.forEach((l) => l.classList.remove("active-work"));
			this.classList.add("active-work");
			onFilterChange(this.innerText as FilterKey);
		}

		linkWork.forEach((l) => l.addEventListener("click", activeWork));

		return () => {
			linkWork.forEach((l) => l.removeEventListener("click", activeWork));
		};
	}, [onFilterChange]);

	return (
		<div className="work__filters">
			<span className="work__item">Upbeat</span>
			<span className="work__item">Ambient</span>
			<span className="work__item">Anxious</span>
			<span className="work__item">Inspiring</span>
		</div>
	);
};

export default WorkFilter;
