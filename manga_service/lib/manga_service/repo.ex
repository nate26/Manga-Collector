defmodule MangaService.Repo do
  use Ecto.Repo,
    otp_app: :manga_service,
    adapter: Ecto.Adapters.Postgres
end
