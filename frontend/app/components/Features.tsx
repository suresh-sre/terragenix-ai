'use client';

import { useState } from 'react';
import TerraformGenerator from './TerraformGenerator';

export default function Features() {
  const [showGenerator, setShowGenerator] = useState(false);

  const features = [
    {
      icon: '⚙️',
      title: 'Generate Infrastructure',
      description: 'Describe your requirements and let AI generate production-ready Terraform code instantly.',
      highlight: 'Terraform AI',
      action: () => setShowGenerator(true)
    },
    {
      icon: '💰',
      title: 'Optimize Cloud Costs',
      description: 'Analyze and reduce cloud spending with intelligent cost optimization recommendations.',
      highlight: 'FinOps'
    },
    {
      icon: '📊',
      title: 'Build Real Projects',
      description: 'Work on real-world DevOps projects and build a professional portfolio.',
      highlight: 'Portfolio Builder'
    },
  ];

  return (
    <>
      <section className="py-20 md:py-32 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16 fade-in">
            <h2 className="text-3xl md:text-5xl font-bold mb-4">
              Everything You Need to Master <span className="gradient-text">DevOps</span>
            </h2>
            <p className="text-lg text-gray-400">Powerful tools designed for the modern cloud engineer</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, idx) => (
              <div
                key={idx}
                className="card fade-in-up cursor-pointer transition-all duration-300 transform hover:scale-105"
                style={{ animationDelay: `${0.2 * (idx + 1)}s` }}
                onClick={feature.action}
              >
                <div className="text-5xl mb-4">{feature.icon}</div>
                <h3 className="text-2xl font-bold mb-2">{feature.title}</h3>
                <p className="text-gray-400 mb-4 leading-relaxed">{feature.description}</p>
                <div className="inline-block px-3 py-1 bg-indigo-500/20 border border-indigo-500/50 rounded-full text-sm text-indigo-300">
                  {feature.highlight}
                </div>
                {feature.action && (
                  <div className="mt-4 text-indigo-400 hover:text-indigo-300 font-semibold text-sm">
                    Try it now →
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Terraform Generator Modal */}
      {showGenerator && (
        <TerraformGenerator onClose={() => setShowGenerator(false)} />
      )}
    </>
  );
}
