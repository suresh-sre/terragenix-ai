export async function POST(request: Request) {
  try {
    const body = await request.json();

    // ===== VALIDATION =====
    if (!body.code || typeof body.code !== 'object') {
      return new Response(
        JSON.stringify({
          error: 'Invalid request',
          details: 'code parameter must be a valid object'
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
          solution: 'Set NEXT_PUBLIC_API_URL in Vercel Settings → Environment Variables to your deployed backend URL.'
        }),
        { status: 503, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // ===== TIMEOUT CONFIGURATION =====
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 9000); // 9 second timeout

    console.log(`[download] Calling backend: ${apiUrl}/download`);
    console.log(`[download] Cloud provider: ${body.cloud_provider}`);
    console.log(`[download] Files to zip: ${Object.keys(body.code).length}`);

    // ===== FETCH REQUEST =====
    let response;
    try {
      response = await fetch(`${apiUrl}/download`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: body.code,
          cloud_provider: body.cloud_provider || 'unknown',
        }),
        signal: controller.signal,
      });
    } catch (fetchError) {
      clearTimeout(timeoutId);

      if (fetchError instanceof Error) {
        if (fetchError.name === 'AbortError') {
          console.error('[download] Request timeout - backend not responding within 9 seconds');
          return new Response(
            JSON.stringify({
              error: 'Backend timeout',
              code: 'BACKEND_TIMEOUT',
              message: 'The backend server is not responding. It may be starting up or experiencing issues.',
              backend_url: apiUrl
            }),
            { status: 504, headers: { 'Content-Type': 'application/json' } }
          );
        }

        console.error('[download] Fetch error:', fetchError.message);
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
      console.error(`[download] Backend returned ${response.status}`);

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

    // ===== SUCCESS - Binary ZIP File =====
    const blob = await response.arrayBuffer();

    console.log(`[download] Success - downloaded ${blob.byteLength} bytes`);

    return new Response(blob, {
      status: 200,
      headers: {
        'Content-Type': 'application/zip',
        'Content-Disposition': `attachment; filename="terraform-${body.cloud_provider || 'download'}-${Date.now()}.zip"`,
      },
    });

  } catch (error) {
    console.error('[download] Unexpected error:', error);

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
