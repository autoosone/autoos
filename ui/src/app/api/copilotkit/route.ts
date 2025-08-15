import { 
  CopilotRuntime, 
  OpenAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";

// CORRECT CONFIGURATION - Following Official Docs
// https://docs.blaxel.ai/Agents/Integrate-in-apps/CopilotKit

const runtime = new CopilotRuntime({
  remoteActions: [
    {
      // PRODUCTION URL - After deployment
      url: process.env.BLAXEL_AGENT_URL || "https://run.blaxel.ai/amo/agents/template-copilot-kit-py/copilotkit",
      headers: {
        "Authorization": `Bearer ${process.env.BLAXEL_API_KEY || "bl_ypbq1x2cdwy272rekcj6017jpvn8o161"}`
      }
    },
  ],
});

const serviceAdapter = new OpenAIAdapter({
  apiKey: process.env.OPENAI_API_KEY || "",
});

export const POST = async (req: Request) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};

export const GET = async () => {
  return new Response(JSON.stringify({ 
    status: "ok",
    agent: "AutoOS Marketplace AI Assistant",
    backend: "Blaxel Agent on Production",
    endpoint: "https://run.blaxel.ai/amo/agents/template-copilot-kit-py/copilotkit",
    documentation: "https://docs.blaxel.ai/Agents/Integrate-in-apps/CopilotKit"
  }), {
    headers: { "Content-Type": "application/json" }
  });
};
