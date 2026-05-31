# --- 1. Define the Central Tool Registry ---

from pprint import pprint


class ToolRegistry:
    def __init__(self):
        # The registry stores tools indexed by their capability
        self.registry = {}

    def register_tool(
        self, tool_name: str, capability: str, endpoint: object,
        schema: dict
    ):
        """Registers a new tool's capability and how to call it."""
        if capability not in self.registry:
            self.registry[capability] = []

        tool_info = {
            "name": tool_name,
            "endpoint": endpoint,
            "schema": schema
        }
        self.registry[capability].append(tool_info)
        print(
            f"REGISTRY: Registered '{tool_name}' with capability '{capability}'.")

    def discover_tools(self, capability: str) -> list:
        """Finds all tools that match a given capability."""
        print(f"REGISTRY: Discovery query for capability '{capability}'.")
        return self.registry.get(capability, [])

# --- 2. Define Mock Tools (as functions) ---


def preferred_vendor_api(part_id: str) -> dict:
    """Internal API for preferred vendors."""
    print(f"   -> TOOL (PreferredVendor): Getting quote for {part_id}...")
    return {"source": "PreferredVendorAPI", "price": 95.00}


def web_scraping_quote_tool(part_id: str) -> dict:
    """Scraping tool for public sites."""
    print(f"   -> TOOL (WebScraper): Getting quote for {part_id}...")
    return {"source": "WebScraper", "price": 98.50}

# --- 3. Setup and Registration ---


# Initialize the central registry
GLOBAL_REGISTRY = ToolRegistry()

# Register the tools
GLOBAL_REGISTRY.register_tool(
    tool_name="PreferredVendorAPITool",
    capability="get_quote",
    endpoint=preferred_vendor_api,
    schema={"part_id": "string"}
)

GLOBAL_REGISTRY.register_tool(
    tool_name="WebScrapingQuoteTool",
    capability="get_quote",
    endpoint=web_scraping_quote_tool,
    schema={"part_id": "string"}
)

# --- 4. Agent Implementation ---


class ProcurementAgent:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def get_best_price(self, part_id: str):
        print(f"\nAGENT: Received task to get best price for {part_id}.")

        # 2. Discovery: Agent queries the registry, not its own code
        capability_to_find = "get_quote"
        found_tools = self.registry.discover_tools(capability_to_find)

        if not found_tools:
            return f"Error: No tools found with capability '{capability_to_find}'."

        print(f"AGENT: Discovered {len(found_tools)} tools. Invoking all...")

        # 3. Invocation: Agent calls the discovered tools
        results = []
        for tool in found_tools:
            # Assumes all tools for 'get_quote' have the same schema
            tool_function = tool["endpoint"]
            result = tool_function(part_id=part_id)
            results.append(result)

        # Agent's reasoning logic to find the best price
        best_quote = min(results, key=lambda x: x["price"])
        print(f"AGENT: Best price found: {best_quote}")
        return best_quote


# --- Execute the Workflow ---
procurement_agent = ProcurementAgent(registry=GLOBAL_REGISTRY)
procurement_agent.get_best_price("Part #XYZ")

pprint(GLOBAL_REGISTRY.registry)
