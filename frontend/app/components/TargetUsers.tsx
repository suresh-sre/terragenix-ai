'use client';

export default function TargetUsers() {
  const users = [
    {
      icon: '🎓',
      title: 'Students',
      description: 'Build real DevOps projects for your resume. Get job-ready with hands-on experience.',
      color: 'from-blue-500/20 to-cyan-500/20'
    },
    {
      icon: '💼',
      title: 'Professionals',
      description: 'Accelerate your cloud career. Generate infrastructure patterns and best practices.',
      color: 'from-purple-500/20 to-pink-500/20'
    },
    {
      icon: '🚀',
      title: 'Startups',
      description: 'Scale infrastructure fast without DevOps overhead. Focus on your product.',
      color: 'from-green-500/20 to-emerald-500/20'
    },
  ];

  return (
    <section className="py-20 md:py-32 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16 fade-in">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">
            Built for <span className="gradient-text">Every Stage</span>
          </h2>
          <p className="text-lg text-gray-400">Whether you are just starting or scaling fast</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {users.map((user, idx) => (
            <div
              key={idx}
              className={`bg-gradient-to-br ${user.color} border border-gray-700 rounded-2xl p-8 hover:border-gray-600 transition-all duration-300 fade-in-up`}
              style={{ animationDelay: `${0.2 * (idx + 1)}s` }}
            >
              <div className="text-6xl mb-4">{user.icon}</div>
              <h3 className="text-2xl font-bold mb-3">{user.title}</h3>
              <p className="text-gray-400 leading-relaxed">{user.description}</p>
              <button className="mt-6 text-indigo-400 hover:text-indigo-300 font-semibold transition-colors">
                Learn more →
              </button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
