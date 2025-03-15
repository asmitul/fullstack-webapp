import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold text-center mb-8">Task Management App</h1>
        <p className="text-center mb-8">A modern task management application built with Next.js and FastAPI</p>
        
        <div className="flex justify-center gap-4">
          <Link href="/login" className="btn btn-primary">
            Login
          </Link>
          <Link href="/register" className="btn btn-secondary">
            Register
          </Link>
        </div>
      </div>
    </main>
  )
} 