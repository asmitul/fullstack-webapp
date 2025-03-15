import Link from 'next/link'

export default function Login() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-md">
        <div>
          <h1 className="text-2xl font-bold text-center">Login to Your Account</h1>
          <p className="mt-2 text-center text-gray-600">
            Enter your credentials to access your account
          </p>
        </div>
        
        <form className="mt-8 space-y-6">
          <div>
            <label htmlFor="email" className="label">
              Email or Username
            </label>
            <input
              id="email"
              name="email"
              type="text"
              required
              className="input"
              placeholder="Email or username"
            />
          </div>
          
          <div>
            <label htmlFor="password" className="label">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              required
              className="input"
              placeholder="Password"
            />
          </div>
          
          <div>
            <button type="submit" className="w-full btn btn-primary">
              Sign in
            </button>
          </div>
        </form>
        
        <div className="text-center mt-4">
          <p className="text-sm text-gray-600">
            Don't have an account?{' '}
            <Link href="/register" className="text-primary-600 hover:text-primary-500">
              Register
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
} 