import Link from 'next/link'

export default function Register() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-md">
        <div>
          <h1 className="text-2xl font-bold text-center">Create an Account</h1>
          <p className="mt-2 text-center text-gray-600">
            Sign up to start managing your tasks
          </p>
        </div>
        
        <form className="mt-8 space-y-6">
          <div>
            <label htmlFor="username" className="label">
              Username
            </label>
            <input
              id="username"
              name="username"
              type="text"
              required
              className="input"
              placeholder="Username"
            />
          </div>
          
          <div>
            <label htmlFor="email" className="label">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              className="input"
              placeholder="Email"
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
            <label htmlFor="confirmPassword" className="label">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              required
              className="input"
              placeholder="Confirm Password"
            />
          </div>
          
          <div>
            <button type="submit" className="w-full btn btn-primary">
              Register
            </button>
          </div>
        </form>
        
        <div className="text-center mt-4">
          <p className="text-sm text-gray-600">
            Already have an account?{' '}
            <Link href="/login" className="text-primary-600 hover:text-primary-500">
              Login
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
} 