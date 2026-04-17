'use client';

export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center px-4 py-12 md:py-20 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-indigo-600/20 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-pink-600/20 rounded-full blur-3xl"></div>
      </div>

      <div className="max-w-4xl mx-auto text-center fade-in">
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
          Build Cloud Infrastructure.{' '}
          <span className="gradient-text">Become DevOps Job-Ready</span> — with AI.
        </h1>

        <p className="text-lg md:text-xl text-gray-400 mb-12 leading-relaxed max-w-2xl mx-auto fade-in-up" style={{ animationDelay: '0.2s' }}>
          Generate Terraform, optimize cloud costs, and build real-world DevOps projects — all in one platform.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12 fade-in-up" style={{ animationDelay: '0.4s' }}>
          <button className="gradient-button">
            Start Building →
          </button>
          <button className="gradient-button-secondary">
            View Demo
          </button>
        </div>

        <p className="text-sm text-gray-500 fade-in-up" style={{ animationDelay: '0.6s' }}>
          ✨ Join 10,000+ DevOps learners building infrastructure with AI
        </p>
      </div>
    </section>
  );
}
