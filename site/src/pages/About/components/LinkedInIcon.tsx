const LinkedInIcon = ({ className = "w-5 h-5" }: { className?: string }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="currentColor"
      className={className}
    >
      <path d="M4.98 3.5C4.98 4.88 3.88 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1 4.98 2.12 4.98 3.5zM.5 8h4V24h-4V8zM8.5 8h3.8v2.16h.05c.53-1 1.84-2.16 3.78-2.16 4.04 0 4.79 2.66 4.79 6.11V24h-4v-7.62c0-1.82-.03-4.16-2.54-4.16-2.54 0-2.93 1.98-2.93 4.03V24h-4V8z" />
    </svg>
  )
}

export default LinkedInIcon
