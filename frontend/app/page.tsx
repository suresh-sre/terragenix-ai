import Header from './components/Header';
import Hero from './components/Hero';
import Features from './components/Features';
import HowItWorks from './components/HowItWorks';
import TargetUsers from './components/TargetUsers';
import WhyUs from './components/WhyUs';
import FinalCTA from './components/FinalCTA';
import Footer from './components/Footer';

export default function Home() {
  return (
    <main className="bg-black text-white overflow-hidden">
      <Header />
      <div className="pt-16">
        <Hero />
        <Features />
        <HowItWorks />
        <TargetUsers />
        <WhyUs />
        <FinalCTA />
        <Footer />
      </div>
    </main>
  );
}