'use client';

import { useState } from 'react';

interface GeneratedCode {
  [key: string]: string;
}

export default function TerraformGenerator({ onClose }: { onClose: () => void }) {
  const [apiKey, setApiKey] = useState('');
  const [cloudProvider, setCloudProvider] = useState<'aws' | 'azure' | 'gcp'>('aws');
  const [services, setServices] = useState('');
  const [requirements, setRequirements] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [generatedCode, setGeneratedCode] = useState<GeneratedCode | null>(null);

  const cloudProviders = [
    { id: 'aws', name: 'AWS', emoji: '☁️' },
    { id: 'azure', name: 'Azure', emoji: '☁️' },
    { id: 'gcp', name: 'GCP', emoji: '☁️' },
  ] as const;

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!apiKey.trim()) {
      setError('Please enter your Gemini API key');
      return;
    }

    if (!services.trim()) {
      setError('Please enter services/resources');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          api_key: apiKey,
          cloud_provider: cloudProvider,
          services: services,
          requirements: requirements,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        // Handle specific error codes
        if (data.code === 'BACKEND_URL_MISSING') {
          throw new Error(
            `❌ Backend Not Configured!\n\nYou need to deploy your backend and add the URL to Vercel:\n\n1. Deploy Python backend to Heroku/Railway\n2. In Vercel Settings → Environment Variables\n3. Add NEXT_PUBLIC_API_URL with your backend URL`
          );
        }
        if (data.code === 'BACKEND_TIMEOUT') {
          throw new Error(
            `⏱️ Backend Not Responding!\n\nThe backend is taking too long or is not running:\n\n1. Check if your backend is deployed\n2. Try visiting your backend URL directly in a browser\n3. Ensure it's running and responding`
          );
        }
        if (data.code === 'BACKEND_CONNECTION_FAILED') {
          throw new Error(
            `🔗 Backend Connection Failed!\n\n${data.message}\n\nVerify your backend URL is correct and the server is running.`
          );
        }

        throw new Error(data.error || `Error: ${response.status}`);
      }

      setGeneratedCode(data.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const copyCode = (code: string) => {
    navigator.clipboard.writeText(code).then(() => {
      alert('Copied to clipboard!');
    });
  };

  const downloadFile = (filename: string, content: string) => {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  const downloadAllAsZip = async () => {
    if (!generatedCode) return;

    try {
      const response = await fetch('/api/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code: generatedCode,
          cloud_provider: cloudProvider,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));

        if (errorData.code === 'BACKEND_TIMEOUT') {
          throw new Error('Backend is not responding. Check if your server is running.');
        }
        if (errorData.code === 'BACKEND_CONNECTION_FAILED') {
          throw new Error(`Cannot connect to backend: ${errorData.message}`);
        }

        throw new Error(errorData.error || 'Download failed');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `terraform-${cloudProvider}-${Date.now()}.zip`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      alert('Failed to download ZIP: ' + (err instanceof Error ? err.message : 'Unknown error'));
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-gray-900 border border-gray-700 rounded-2xl max-w-4xl w-full my-8">
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b border-gray-700">
          <h2 className="text-2xl font-bold">
            <span className="gradient-text">Generate Terraform Code</span>
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors text-2xl"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-6 max-h-[calc(100vh-200px)] overflow-y-auto">
          {!generatedCode ? (
            <form onSubmit={handleGenerate} className="space-y-6">
              {/* API Key Input */}
              <div>
                <label className="block text-sm font-semibold mb-2">
                  🔑 Gemini API Key
                </label>
                <input
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="Enter your Gemini API Key"
                  className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
                />
                <p className="text-xs text-gray-400 mt-1">
                  Get free API key from{' '}
                  <a
                    href="https://aistudio.google.com/app/apikey"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-indigo-400 hover:text-indigo-300"
                  >
                    Google AI Studio
                  </a>
                </p>
              </div>

              {/* Cloud Provider Selection */}
              <div>
                <label className="block text-sm font-semibold mb-3">
                  ☁️ Select Cloud Provider
                </label>
                <div className="grid grid-cols-3 gap-3">
                  {cloudProviders.map((provider) => (
                    <button
                      key={provider.id}
                      type="button"
                      onClick={() => setCloudProvider(provider.id)}
                      className={`p-4 rounded-lg border-2 transition-all ${
                        cloudProvider === provider.id
                          ? 'border-indigo-500 bg-indigo-500/20 text-white'
                          : 'border-gray-600 bg-gray-800 text-gray-400 hover:border-gray-500'
                      }`}
                    >
                      <div className="text-2xl mb-1">{provider.emoji}</div>
                      <div className="font-semibold">{provider.name}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Services Input */}
              <div>
                <label className="block text-sm font-semibold mb-2">
                  🛠️ Services/Resources (comma or line separated)
                </label>
                <textarea
                  value={services}
                  onChange={(e) => setServices(e.target.value)}
                  placeholder={`Examples:\nAWS: ec2, rds, s3, vpc, lambda\nAzure: vm, sql-database, storage-account\nGCP: compute-instance, cloud-sql, storage-bucket`}
                  rows={5}
                  className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 font-mono text-sm"
                />
              </div>

              {/* Requirements Input */}
              <div>
                <label className="block text-sm font-semibold mb-2">
                  📋 Additional Requirements (Optional)
                </label>
                <textarea
                  value={requirements}
                  onChange={(e) => setRequirements(e.target.value)}
                  placeholder="Example: Use t3.micro for EC2, enable encryption, add tags for production, use us-east-1 region"
                  rows={3}
                  className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 font-mono text-sm"
                />
              </div>

              {/* Error Message */}
              {error && (
                <div className="bg-red-500/20 border border-red-500 text-red-100 rounded-lg p-4 text-sm whitespace-pre-wrap font-mono">
                  {error}
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full gradient-button disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? '🔄 Generating...' : '🚀 Generate Terraform Code'}
              </button>
            </form>
          ) : (
            <div className="space-y-4">
              {/* Generated Code Output */}
              {Object.entries(generatedCode).map(([filename, content]) => (
                <div key={filename}>
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="font-semibold text-indigo-400">📄 {filename}</h3>
                    <div className="flex gap-2">
                      <button
                        onClick={() => copyCode(content as string)}
                        className="text-xs bg-indigo-600 hover:bg-indigo-700 px-3 py-1 rounded transition-colors"
                      >
                        📋 Copy
                      </button>
                      <button
                        onClick={() => downloadFile(filename, content as string)}
                        className="text-xs bg-gray-700 hover:bg-gray-600 px-3 py-1 rounded transition-colors"
                      >
                        📥 Download
                      </button>
                    </div>
                  </div>
                  <pre className="bg-gray-800 border border-gray-700 rounded-lg p-4 overflow-x-auto text-xs text-gray-300">
                    <code>{content}</code>
                  </pre>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="border-t border-gray-700 p-6 bg-gray-800/50 rounded-b-2xl flex justify-end gap-3">
          {generatedCode && (
            <button
              onClick={() => setGeneratedCode(null)}
              className="gradient-button-secondary px-6 py-2"
            >
              🔄 Generate New
            </button>
          )}
          {generatedCode && (
            <button
              onClick={downloadAllAsZip}
              className="gradient-button px-6 py-2"
            >
              📦 Download ZIP
            </button>
          )}
          {!generatedCode && (
            <button
              onClick={onClose}
              className="gradient-button-secondary px-6 py-2"
            >
              Close
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
