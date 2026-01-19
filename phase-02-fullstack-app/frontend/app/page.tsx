/**
 * Home page - Landing page with links to authentication.
 */
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-xl shadow-lg">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Todo App
          </h1>
          <p className="text-lg text-gray-600 mb-8">
            Phase II - Full-Stack Web Application
          </p>
          <p className="text-sm text-gray-500 mb-8">
            Manage your tasks efficiently with our secure, multi-user todo application.
          </p>
        </div>

        <div className="space-y-4">
          <Link
            href="/auth/signin"
            className="block w-full py-3 px-4 text-center text-white bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-colors"
          >
            Sign In
          </Link>
          <Link
            href="/auth/signup"
            className="block w-full py-3 px-4 text-center text-blue-600 bg-white border-2 border-blue-600 hover:bg-blue-50 rounded-lg font-medium transition-colors"
          >
            Create Account
          </Link>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-200">
          <h2 className="text-sm font-semibold text-gray-900 mb-3">Features:</h2>
          <ul className="space-y-2 text-sm text-gray-600">
            <li className="flex items-center">
              <svg className="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Create, update, and delete tasks
            </li>
            <li className="flex items-center">
              <svg className="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Mark tasks as complete
            </li>
            <li className="flex items-center">
              <svg className="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Secure authentication with JWT
            </li>
            <li className="flex items-center">
              <svg className="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Private task lists per user
            </li>
          </ul>
        </div>

        <div className="text-center text-xs text-gray-500 mt-8">
          <p>Built with Next.js 16, FastAPI, and PostgreSQL</p>
        </div>
      </div>
    </div>
  );
}
