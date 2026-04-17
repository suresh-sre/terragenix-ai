'use client';

export default function FinalCTA() {
  return (
    <section className="py-20 md:py-32 px-4">
      <div className="max-w-4xl mx-auto text-center">
        <div className="mb-12 fade-in">
          <h2 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
            Start Building Your <span className="gradient-text">DevOps Future</span> Today
          </h2>
          <p className="text-lg md:text-xl text-gray-400 mb-8 leading-relaxed">
            Join thousands of DevOps learners and professionals building infrastructure with AI.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12 fade-in-up" style={{ animationDelay: '0.2s' }}>
          <button className="gradient-button">
            Start Free Now →
          </button>
          <button className="gradient-button-secondary">
            Schedule a Demo
          </button>
        </div>

        <p className="text-sm text-gray-500 fade-in-up" style={{ animationDelay: '0.4s' }}>
          No credit card required • 14-day free trial • Full access to all features
        </p>

        <div className="mt-16 pt-12 border-t border-gray-800 fade-in-up" style={{ animationDelay: '0.6s' }}>
          <p className="text-gray-500 text-sm mb-6">Trusted by leading organizations</p>
          <div className="flex justify-center items-center gap-8 flex-wrap opacity-60 hover:opacity-100 transition-opacity">
            <div className="text-gray-600 font-semibold">Acme Corp</div>
            <div className="text-gray-600 font-semibold">TechStart</div>
            <div className="text-gray-600 font-semibold">CloudFlare</div>
            <div className="text-gray-600 font-semibold">DevOps.io</div>
          </div>
        </div>
      </div>
    </section>
  );
}
