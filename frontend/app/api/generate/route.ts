export async function POST(request: Request) {
  try {
    const body = await request.json();

    // ===== VALIDATION =====
    // Check required fields
    if (!body.api_key || !body.cloud_provider || !body.services) {
      return new Response(
        JSON.stringify({
          error: 'Missing required fields',
          details: 'api_key, cloud_provider, and services are required'
        }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // ===== CONFIGURATION =====
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;

    if (!apiUrl) {
      console.error('CRITICAL: NEXT_PUBLIC_API_URL environment variable not set');
      return new Response(
        JSON.stringify({
          error: 'Backend not configured',
          code: 'BACKEND_URL_MISSING',
          message: 'Backend API URL is not configured in Vercel environment variables.',
          solution: 'Set NEXT_PUBLIC_API_URL in Vercel Settings → Environment Variables to your deployed backend URL (e.g., https://your-api.herokuapp.com)'
        }),
        { status: 503, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // ===== TIMEOUT CONFIGURATION =====
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 9000); // 9 second timeout (leave 1s margin)

    console.log(`[generate] Calling backend: ${apiUrl}/generate`);
    console.log(`[generate] Cloud provider: ${body.cloud_provider}`);
    console.log(`[generate] Services: ${body.services}`);

    // ===== FETCH REQUEST =====
    let response;
    try {
      response = await fetch(`${apiUrl}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          api_key: body.api_key,
          cloud_provider: body.cloud_provider,
          services: body.services,
          requirements: body.requirements || '',
        }),
        signal: controller.signal,
      });
    } catch (fetchError) {
      clearTimeout(timeoutId);

      if (fetchError instanceof Error) {
        if (fetchError.name === 'AbortError') {
          console.error('[generate] Request timeout - backend not responding within 9 seconds');
          return new Response(
            JSON.stringify({
              error: 'Backend timeout',
              code: 'BACKEND_TIMEOUT',
              message: 'The backend server is not responding. It may be starting up or experiencing issues.',
              solution: 'Check if your backend is deployed and running. Visit your backend URL directly in a browser.',
              backend_url: apiUrl
            }),
            { status: 504, headers: { 'Content-Type': 'application/json' } }
          );
        }

        console.error('[generate] Fetch error:', fetchError.message);
        return new Response(
          JSON.stringify({
            error: 'Backend connection failed',
            code: 'BACKEND_CONNECTION_FAILED',
            message: fetchError.message,
            backend_url: apiUrl
          }),
          { status: 502, headers: { 'Content-Type': 'application/json' } }
        );
      }
      throw fetchError;
    } finally {
      clearTimeout(timeoutId);
    }

    // ===== RESPONSE HANDLING =====
    if (!response.ok) {
      console.error(`[generate] Backend returned ${response.status}`);

      let errorData;
      try {
        errorData = await response.json();
      } catch {
        errorData = { error: `Backend error ${response.status}` };
      }

      return new Response(
        JSON.stringify({
          error: errorData.error || `Backend error: ${response.status}`,
          details: errorData.details || null,
          backend_status: response.status
        }),
        { status: response.status, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // ===== SUCCESS =====
    let data;
    try {
      data = await response.json();
    } catch (parseError) {
      console.error('[generate] Failed to parse backend response as JSON');
      return new Response(
        JSON.stringify({
          error: 'Invalid backend response',
          code: 'INVALID_RESPONSE',
          message: 'Backend returned invalid JSON'
        }),
        { status: 502, headers: { 'Content-Type': 'application/json' } }
      );
    }

    console.log('[generate] Success - returning generated code');
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });

  } catch (error) {
    console.error('[generate] Unexpected error:', error);

    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    const errorStack = error instanceof Error ? error.stack : '';

    return new Response(
      JSON.stringify({
        error: 'Internal server error',
        code: 'INTERNAL_ERROR',
        message: errorMessage,
        stack: process.env.NODE_ENV === 'development' ? errorStack : undefined
      }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}
