interface PaginationProps {
  currentPage: number
  totalPages: number
  onPageChange: (page: number) => void
}

const Pagination = ({ currentPage, totalPages, onPageChange }: PaginationProps) => {
  const handlePageChange = (page: number) => {
    onPageChange(page)
    window.scrollTo({ top: 0, behavior: "smooth" })
  }

  const navButtonClasses =
    "py-2.5 px-5 border border-[#e5e5e5] bg-white text-[#1a1a1a] cursor-pointer rounded-lg text-[0.9375rem] font-medium transition-all hover:bg-[#f6f6ed] hover:border-[#1a7f4e] hover:text-[#1a7f4e] disabled:opacity-40 disabled:cursor-not-allowed disabled:text-[#999] max-sm:py-2 max-sm:px-3.5 max-sm:text-sm"

  return (
    <div className="flex justify-center items-center gap-2 mt-8 p-6 bg-white rounded-xl border border-[#e5e5e5] max-sm:flex-wrap max-sm:gap-1.5">
      <button
        className={navButtonClasses}
        disabled={currentPage === 1}
        onClick={() => handlePageChange(currentPage - 1)}
      >
        ← Anterior
      </button>

      <div className="flex gap-1.5 items-center">
        {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => {
          const showPage =
            page === 1 ||
            page === totalPages ||
            Math.abs(page - currentPage) <= 1

          if (!showPage && page === currentPage - 2) {
            return (
              <span key={`ellipsis-${page}`} className="p-2 text-[#999] font-medium">
                ...
              </span>
            )
          }

          if (!showPage && page === currentPage + 2) {
            return (
              <span key={`ellipsis-${page}`} className="p-2 text-[#999] font-medium">
                ...
              </span>
            )
          }

          if (!showPage) return null

          const isActive = currentPage === page

          return (
            <button
              key={page}
              className={`min-w-10 h-10 p-2 border cursor-pointer rounded-lg text-[0.9375rem] font-medium transition-all flex items-center justify-center max-sm:min-w-9 max-sm:h-9 max-sm:text-sm ${
                isActive
                  ? "bg-[#1a7f4e] text-white border-[#1a7f4e] font-semibold"
                  : "bg-white text-[#1a1a1a] border-[#e5e5e5] hover:bg-[#f6f6ed] hover:border-[#1a7f4e] hover:text-[#1a7f4e]"
              }`}
              onClick={() => handlePageChange(page)}
            >
              {page}
            </button>
          )
        })}
      </div>

      <button
        className={navButtonClasses}
        disabled={currentPage === totalPages}
        onClick={() => handlePageChange(currentPage + 1)}
      >
        Próxima →
      </button>
    </div>
  )
}

export default Pagination
