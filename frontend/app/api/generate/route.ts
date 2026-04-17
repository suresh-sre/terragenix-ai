export async function POST(request: Request) {
  try {
    const body = await request.json();

    // Get the API backend URL from environment
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;

    // In production, NEXT_PUBLIC_API_URL must be set
    if (!apiUrl) {
      return new Response(
        JSON.stringify({
          error: 'Backend API URL not configured. Please set NEXT_PUBLIC_API_URL environment variable.',
          details: 'Deploy backend to Heroku/Railway/AWS and set the URL in Vercel environment variables.'
        }),
        { status: 503, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const response = await fetch(`${apiUrl}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        api_key: body.api_key,
        cloud_provider: body.cloud_provider,
        services: body.services,
        requirements: body.requirements,
      }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      return new Response(
        JSON.stringify({ error: error.error || `Backend error: ${response.status}` }),
        { status: response.status, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const data = await response.json();
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error('Generate API error:', error);
    return new Response(
      JSON.stringify({
        error: error instanceof Error ? error.message : 'Internal server error',
      }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}
