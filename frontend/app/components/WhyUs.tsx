'use client';

export default function WhyUs() {
  const reasons = [
    {
      icon: '🤖',
      title: 'AI-Powered DevOps',
      description: 'Generate infrastructure code in seconds, not days. AI learns your patterns.',
    },
    {
      icon: '🌍',
      title: 'Real-World Projects',
      description: 'Work on production-like scenarios. Build a portfolio that impresses employers.',
    },
    {
      icon: '💡',
      title: 'Cost-Aware Design',
      description: 'Learn to build cloud infrastructure that is efficient and cost-optimized.',
    },
    {
      icon: '📈',
      title: 'Career-Focused',
      description: 'Track your learning journey. Showcase your DevOps skills to employers.',
    },
  ];

  return (
    <section className="py-20 md:py-32 px-4 bg-gradient-to-b from-transparent via-pink-950/10 to-transparent">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-16 fade-in">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">
            Why <span className="gradient-text">GenOpsLab</span>?
          </h2>
          <p className="text-lg text-gray-400">The platform designed for DevOps success</p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {reasons.map((reason, idx) => (
            <div
              key={idx}
              className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 border border-gray-700 rounded-xl p-8 hover:border-indigo-500/50 transition-all duration-300 fade-in-up"
              style={{ animationDelay: `${0.15 * (idx + 1)}s` }}
            >
              <div className="text-4xl mb-4">{reason.icon}</div>
              <h3 className="text-xl font-bold mb-2">{reason.title}</h3>
              <p className="text-gray-400 leading-relaxed">{reason.description}</p>
            </div>
          ))}
        </div>

        <div className="mt-16 bg-gradient-to-r from-indigo-600/20 to-pink-600/20 border border-indigo-500/30 rounded-2xl p-8 md:p-12 text-center fade-in-up" style={{ animationDelay: '0.8s' }}>
          <h3 className="text-2xl md:text-3xl font-bold mb-2">Missing something?</h3>
          <p className="text-gray-400 mb-6">We are constantly adding new features based on community feedback</p>
          <button className="text-indigo-400 hover:text-indigo-300 font-semibold transition-colors">
            Join our Discord community →
          </button>
        </div>
      </div>
    </section>
  );
}
