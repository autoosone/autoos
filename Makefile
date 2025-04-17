install:
	for dir in crew-flight-agent langgraph-hotel-agent explorer-mcp .; do \
		cd $$dir && uv venv && uv sync && cd ..; \
	done

run:
	bl serve --hotreload

run_supervisor:
	bl serve --hotreload --recursive=false

run_flight_agent:
	cd crew-flight-agent && \
		bl serve --hotreload --recursive=false

run_hotel_agent:
	cd langgraph-hotel-agent && \
		bl serve --hotreload --recursive=false

run_explorer_mcp:
	cd explorer-mcp && \
		bl serve --hotreload --recursive=false

dev_explorer_mcp:
	cd explorer-mcp && BL_DEBUG=true uv run mcp dev src/server.py

deploy:
	bl deploy

deploy_flight_agent:
	cd crew-flight-agent && bl deploy --recursive=false

deploy_hotel_agent:
	cd langgraph-hotel-agent && bl deploy --recursive=false

deploy_explorer_mcp:
	cd explorer-mcp && bl deploy --recursive=false



PHONY: install run_supervisor run_flight_agent run_hotel_agent run_explorer_mcp deploy deploy_flight_agent deploy_hotel_agent deploy_explorer_mcp
