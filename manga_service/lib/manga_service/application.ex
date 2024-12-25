defmodule MangaService.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      MangaServiceWeb.Telemetry,
      MangaService.Repo,
      {DNSCluster, query: Application.get_env(:manga_service, :dns_cluster_query) || :ignore},
      {Phoenix.PubSub, name: MangaService.PubSub},
      # Start the Finch HTTP client for sending emails
      {Finch, name: MangaService.Finch},
      # Start a worker by calling: MangaService.Worker.start_link(arg)
      # {MangaService.Worker, arg},
      # Start to serve requests, typically the last entry
      MangaServiceWeb.Endpoint
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: MangaService.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  @impl true
  def config_change(changed, _new, removed) do
    MangaServiceWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
