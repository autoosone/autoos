import { 
  CopilotRuntime, 
  OpenAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";

const runtime = new CopilotRuntime({
  remoteActions: [
    {
      url: "http://localhost:1338/copilotkit",
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