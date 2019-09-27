from app import instance
import app.config

if __name__ == '__main__':
	conf = app.config.Config()
	instance.run(host=conf.HOST, port=conf.PORT, debug=conf.DEBUG)

