import { Link } from "react-router-dom";
import "./AboutPage.css";

const SERVICES = [
    {
        title: "Web Development",
        text: "Responsive websites, e-commerce stores, web applications and dashboards.",
    },
    {
        title: "Mobile App Development",
        text: "Android, iOS and cross-platform apps built with Flutter and React Native.",
    },
    {
        title: "AI/ML Solutions",
        text: "Chatbots, recommendation systems, predictive analytics and LLM-powered tools.",
    },
    {
        title: "Cloud Services",
        text: "Migration, deployment, monitoring and cost optimisation on AWS, Azure and Google Cloud.",
    },
    {
        title: "UI/UX Design",
        text: "User research, wireframes, prototypes and design systems.",
    },
];

function AboutPage() {
    return (
        <div className="about-page">
            <div className="about-card">
                <header className="about-header">
                    <div>
                        <h1>About Resolven Technologies</h1>
                        <p>The company behind Resolv.ai</p>
                    </div>
                    <Link to="/" className="back-link">
                        ← Back to chat
                    </Link>
                </header>

                <section>
                    <h2>Who we are</h2>
                    <p>
                        Founded in 2026 and headquartered in Bengaluru, India, Resolven
                        Technologies is a team of about 120 engineers, designers and AI
                        specialists. Our mission is to help businesses grow through
                        reliable, modern technology. (Resolven is a fictional company
                        created for this demo.)
                    </p>
                </section>

                <section>
                    <h2>Our services</h2>
                    <div className="service-grid">
                        {SERVICES.map((s) => (
                            <div key={s.title} className="service-card">
                                <h3>{s.title}</h3>
                                <p>{s.text}</p>
                            </div>
                        ))}
                    </div>
                </section>

                <section>
                    <h2>Contact support</h2>
                    <ul>
                        <li>Hours: Monday to Friday, 9:00 AM to 6:00 PM IST</li>
                        <li>Email: support@resolven.example</li>
                        <li>Phone: +91 80 0000 0000</li>
                    </ul>
                </section>
            </div>
        </div>
    );
}

export default AboutPage;