export async function POST(request: Request) {
  try {
    const body = await request.json();

    // Get the API backend URL from environment or use default
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

    const response = await fetch(`${apiUrl}/download`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        code: body.code,
        cloud_provider: body.cloud_provider,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      return new Response(
        JSON.stringify({ error: error.error || 'Download failed' }),
        { status: response.status, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const blob = await response.arrayBuffer();
    return new Response(blob, {
      status: 200,
      headers: {
        'Content-Type': 'application/zip',
        'Content-Disposition': `attachment; filename="terraform-${body.cloud_provider}-${Date.now()}.zip"`,
      },
    });
  } catch (error) {
    console.error('Download API error:', error);
    return new Response(
      JSON.stringify({
        error: error instanceof Error ? error.message : 'Internal server error',
      }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}
