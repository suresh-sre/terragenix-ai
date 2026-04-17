'use client';

export default function HowItWorks() {
  const steps = [
    {
      number: '01',
      title: 'Describe Your Infrastructure',
      description: 'Tell GenOpsLab what you want to build. Simple, natural language.',
    },
    {
      number: '02',
      title: 'Generate Terraform Code',
      description: 'AI instantly creates production-ready Terraform configurations.',
    },
    {
      number: '03',
      title: 'Analyze Cloud Costs',
      description: 'See detailed cost breakdowns and optimization recommendations.',
    },
    {
      number: '04',
      title: 'Deploy & Learn',
      description: 'Deploy your infrastructure and track it in your DevOps portfolio.',
    },
  ];

  return (
    <section className="py-20 md:py-32 px-4 bg-gradient-to-b from-transparent via-indigo-950/10 to-transparent">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16 fade-in">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">
            How <span className="gradient-text">GenOpsLab</span> Works
          </h2>
          <p className="text-lg text-gray-400">Four simple steps to DevOps mastery</p>
        </div>

        <div className="grid md:grid-cols-4 gap-6 md:gap-4">
          {steps.map((step, idx) => (
            <div key={idx} className="relative fade-in-up" style={{ animationDelay: `${0.15 * (idx + 1)}s` }}>
              {/* Connector line */}
              {idx < steps.length - 1 && (
                <div className="hidden md:block absolute top-12 left-[60%] w-[40%] h-1 bg-gradient-to-r from-indigo-500 to-transparent"></div>
              )}

              {/* Step card */}
              <div className="relative z-10 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 rounded-2xl p-6 hover:border-indigo-500/60 transition-all duration-300">
                <div className="text-4xl font-bold gradient-text mb-4">{step.number}</div>
                <h3 className="text-xl font-bold mb-3">{step.title}</h3>
                <p className="text-gray-400 text-sm leading-relaxed">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
